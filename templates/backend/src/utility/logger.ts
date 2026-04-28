import pinoModule from "pino";
import type { LoggerOptions, Logger } from "pino";

const pino = pinoModule.pino || (pinoModule as any);
import { AsyncLocalStorage } from "async_hooks";
import { v4 as uuidv4 } from "uuid";
import type { Request, Response, NextFunction } from "express";

// ====== 1. pino config ======
const loggerConfig: LoggerOptions = {
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level(label: string) {
      return { level: label.toUpperCase() };
    },
    bindings() {
      return {};
    }
  },
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
      translateTime: "HH:mm:ss.l",
      ignore: "pid,hostname",
      messageFormat: "{msg}",
      singleLine: true
    }
  }
};

// ====== 2. logger with async context ======
export const loggerPino: Logger = pino(loggerConfig);

interface RequestContext {
  requestId?: string;
  userId?: string;
  email?: string;
  userType?: string;
}

const asyncLocal = new AsyncLocalStorage<RequestContext>();
const getContext = (): RequestContext => asyncLocal.getStore() || {};

// Use loggerPino directly with child bindings from context
const logger = new Proxy(loggerPino, {
  get(target, prop, receiver) {
    const context = getContext();
    if (Object.keys(context).length > 0) {
      return Reflect.get(target.child(context), prop, receiver);
    }
    return Reflect.get(target, prop, receiver);
  }
});

// ====== 3. AsyncLocalStorage run helper ======
export const clsRun = <T>(context: RequestContext, fn: () => T): T => asyncLocal.run(context, fn);

// ====== 4. Request logger middleware ======
export const requestLogger = () => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const requestId = (req.headers["x-request-id"] as string) || uuidv4();

    const context: RequestContext = {
      requestId,
      userId: (req as any).user?.userId,
      email: (req as any).user?.email,
      userType: (req as any).user?.userType
    };

    clsRun(context, () => {
      const startTime = Date.now();
      const originalJson = res.json;
      let responseBody: any = null;

      res.json = function (body: any) {
        responseBody = body;
        return originalJson.call(this, body);
      };

      const reqId = requestId.substring(0, 8);

      const shouldSkipLog =
        req.originalUrl === "/health" ||
        req.originalUrl.startsWith("/public/") ||
        req.originalUrl.includes("favicon.ico");

      if (!shouldSkipLog) {
        const startMsg = `[requestId: ${reqId}][timestamp: ${startTime}] START ${req.method} ${req.originalUrl}`;
        logger.info(startMsg);

        if (
          Object.keys(req.body || {}).length > 0 ||
          Object.keys(req.query || {}).length > 0
        ) {
          logger.info({
            requestId: reqId,
            timestamp: startTime,
            method: req.method,
            path: req.originalUrl,
            phase: "START",
            body: req.body,
            query: req.query
          });
        }
      }

      res.on("finish", () => {
        const endTime = Date.now();
        const duration = endTime - startTime;
        const statusCode = res.statusCode;

        if (shouldSkipLog) return;

        const finalUserId = (req as any).user?.userId;
        const userPrefix = finalUserId ? `[userId: ${finalUserId}]` : "[userId: null]";

        const logData = {
          requestId: reqId,
          timestamp: endTime,
          userId: finalUserId,
          email: (req as any).user?.email,
          userType: (req as any).user?.userType,
          method: req.method,
          path: req.originalUrl,
          statusCode: statusCode,
          duration: duration,
          phase: "END",
          responseBody: responseBody
        };

        let logLevel: "info" | "error" | "warn" = "info";
        let endMsg = "";

        if (statusCode >= 400) {
          logLevel = "error";
          endMsg = `[requestId: ${reqId}][timestamp: ${endTime}]${userPrefix} ERROR ${req.method} ${req.originalUrl} [${statusCode}] ${duration}ms`;
        } else if (duration > 3000) {
          logLevel = "warn";
          endMsg = `[requestId: ${reqId}][timestamp: ${endTime}]${userPrefix} SLOW ${req.method} ${req.originalUrl} [${statusCode}] ${duration}ms`;
        } else {
          logLevel = "info";
          endMsg = `[requestId: ${reqId}][timestamp: ${endTime}]${userPrefix} END ${req.method} ${req.originalUrl} [${statusCode}] ${duration}ms`;
        }

        logger[logLevel](logData);
        logger[logLevel](endMsg);
      });

      res.on("error", (error: Error) => {
        const errorTime = Date.now();
        const finalUserId = (req as any).user?.userId;
        const userPrefix = finalUserId ? `[userId: ${finalUserId}]` : "[userId: null]";

        logger.error({
          err: error,
          requestId: reqId,
          timestamp: errorTime,
          userId: finalUserId,
          email: (req as any).user?.email,
          userType: (req as any).user?.userType,
          method: req.method,
          path: req.originalUrl,
          phase: "ERROR"
        });

        logger.error(
          `[requestId: ${reqId}][timestamp: ${errorTime}]${userPrefix} ERROR ${req.method} ${req.originalUrl}`
        );
      });

      next();
    });
  };
};

// ====== 5. Error logger middleware ======
export const errorLogger = () => {
  return (error: Error, req: Request, _res: Response, next: NextFunction) => {
    const errorTime = Date.now();
    const requestId = (req.headers["x-request-id"] as string) || "unknown";
    const reqId = requestId.substring(0, 8);
    const userId = (req as any).user?.userId;
    const userPrefix = userId ? `[userId: ${userId}]` : "[userId: null]";

    logger.error({
      err: error,
      requestId: reqId,
      timestamp: errorTime,
      userId: userId,
      email: (req as any).user?.email,
      userType: (req as any).user?.userType,
      method: req.method,
      path: req.originalUrl,
      phase: "APPLICATION_ERROR"
    });

    logger.error(
      `[requestId: ${reqId}][timestamp: ${errorTime}]${userPrefix} APPLICATION ERROR ${req.method} ${req.originalUrl}`
    );

    next(error);
  };
};

// ====== 6. Helper functions ======
export const logDetail = (message: string, details: unknown) => {
  logger.info(message, { details });
};

export const logError = (message: string, error: Error, context: object = {}) => {
  logger.error({ err: error, ...context }, message);
};

export default logger;
