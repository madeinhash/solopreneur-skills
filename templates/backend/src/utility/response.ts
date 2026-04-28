import { Response } from "express";
import { isProd } from "./env.js";

const response = (
  res: Response,
  statusCode: number,
  message: unknown = null,
  data: unknown = null,
  debug: unknown = null
) => {
  return res.status(statusCode).json({
    statusCode: statusCode,
    message: message,
    data: data,
    requestId: (res.req as any).requestId,
    ...(!isProd() && { debug })
  });
};

export default response;
