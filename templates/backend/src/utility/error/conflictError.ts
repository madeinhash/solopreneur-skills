import { HTTP_STATUS_CODE } from "../httpStatusCode.js";
import { BaseError } from "./baseError.js";

export class ConflictError extends BaseError {
  constructor(message: string) {
    super("ConflictError", HTTP_STATUS_CODE.CONFLICT, message);
  }
}
