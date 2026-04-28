import express from "express";
import cookieParser from "cookie-parser";
import logger, { requestLogger, errorLogger } from "./utility/logger.js";
import cors from "cors";
import helmet from "helmet";
import response from "./utility/response.js";
import router from "./router/index.js";
import { HTTP_STATUS_CODE } from "./utility/httpStatusCode.js";
import { db } from "./db/sequelizeConfig.js";

const conn = await db();
const app = express();

app.use(helmet());
app.use(cors({ origin: process.env.CORS_WHITELIST?.split(",") }));
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true, limit: "10mb" }));
app.use(cookieParser());

app.use(requestLogger());

app.get("/health", async (_req, res) => {
  return response(res, HTTP_STATUS_CODE.OK, { status: "Healthy", version: "1.0.0" });
});

// API routes
app.use("/api", router);

// Error handling middleware
app.use(errorLogger());

app.use((err: any, _req: express.Request, res: express.Response, next: express.NextFunction) => {
  if (err) {
    (res as any).err = err;
    const statusCode = err.statusCode || HTTP_STATUS_CODE.INTERNAL_SERVER_ERROR;
    const message = err.message || "Internal Error";

    return response(res, statusCode, message, null, {
      error: {
        type: err.name,
        message: err.message,
        stack: err.stack
      }
    });
  }
  return next();
});

app.listen(process.env.PORT, () => {
  logger.info(`${process.env.NODE_ENV} Started server on port ${process.env.PORT}`);
});

export default app;
