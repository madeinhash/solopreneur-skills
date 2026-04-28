import { HTTP_STATUS_CODE } from "../httpStatusCode.js";
import { BaseError } from "./baseError.js";

export class NotFoundError extends BaseError {
  constructor(message: string) {
    super("NotFoundError", HTTP_STATUS_CODE.NOT_FOUND, message);
  }
}
