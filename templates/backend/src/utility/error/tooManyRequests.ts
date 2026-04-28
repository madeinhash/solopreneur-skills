import { HTTP_STATUS_CODE } from "../httpStatusCode.js";
import { BaseError } from "./baseError.js";

export class TooManyRequestsError extends BaseError {
  constructor(message: string) {
    super("TooManyRequestsError", HTTP_STATUS_CODE.TOO_MANY_REQUESTS, message);
  }
}
