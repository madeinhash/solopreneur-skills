import crypto from "crypto";
import jwt from "jsonwebtoken";
import logger from "./logger.js";

const defaultJWTKey = "RgVRWFBHGShlnOFHukepzL2axpkp9epV";

const jwtKey = process.env.JWT_SECRET ? process.env.JWT_SECRET : defaultJWTKey;

const sha256 = (input: string): string => {
  return crypto.createHash("sha256").update(input).digest("hex");
};

interface JwtVerifyResult {
  code: number;
  msg: string;
  login: boolean;
  data?: any;
  err?: string;
}

const verifyJwtToken = (token: string): JwtVerifyResult => {
  try {
    const decoded = jwt.verify(token, jwtKey);

    return {
      code: 200,
      msg: "login success",
      login: true,
      data: decoded
    };
  } catch (err: any) {
    logger.error("JWT validation error:", err.message);

    if (err.name === "TokenExpiredError") {
      return {
        code: 401,
        msg: "Login timeout, please login again",
        login: false,
        err: err.message
      };
    }

    return {
      code: 500,
      msg: "Login fail",
      login: false,
      err: err.message
    };
  }
};

const createUserJwtToken = async (data: object, exp: jwt.SignOptions): Promise<string> =>
  jwt.sign(data, jwtKey, exp);

export { jwt, jwtKey, sha256, verifyJwtToken, createUserJwtToken };
