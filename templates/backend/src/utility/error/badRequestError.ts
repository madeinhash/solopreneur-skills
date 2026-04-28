import { HTTP_STATUS_CODE } from "../httpStatusCode.js";
import { BaseError } from "./baseError.js";

export class BadRequestError extends BaseError {
  constructor(message: string) {
    super("BadRequestError", HTTP_STATUS_CODE.BAD_REQUEST, message);
  }
}
