import { Request, Response, NextFunction } from "express";
import { verifyJwtToken } from "../utility/serverJwt.js";

const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  let token: string | undefined;

  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith("Bearer ")) {
    token = authHeader.split(" ")[1];
  } else if (req.query.token) {
    token = req.query.token as string;
  }

  if (!token) {
    return res.status(401).json({
      message: "Missing or invalid Authorization header",
      login: false
    });
  }

  const result = verifyJwtToken(token);

  if (!result.login) {
    return res.status(result.code).json({
      message: result.msg,
      error: result.err,
      login: false
    });
  }

  (req as any).user = result.data;
  next();
};

export const checkJWT = authMiddleware;
export default authMiddleware;
