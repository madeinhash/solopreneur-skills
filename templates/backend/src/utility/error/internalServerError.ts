import { HTTP_STATUS_CODE } from "../httpStatusCode.js";
import { BaseError } from "./baseError.js";

export class InternalServerError extends BaseError {
  constructor(message: string) {
    super("InternalServerError", HTTP_STATUS_CODE.INTERNAL_SERVER_ERROR, message);
  }
}
