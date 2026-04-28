import { HTTP_STATUS_CODE } from "../httpStatusCode.js";
import { BaseError } from "./baseError.js";

export class ForbiddenError extends BaseError {
  constructor(message: string) {
    super("ForbiddenError", HTTP_STATUS_CODE.FORBIDDEN, message);
  }
}
