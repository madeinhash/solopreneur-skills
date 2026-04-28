// Example User Router
import express from "express";
import { getProfile, updateProfile } from "../controller/user.example.js";
import { checkJWT } from "../middleware/checkJWTMiddleWare.js";

const router = express.Router();

// All routes require authentication
router.use(checkJWT);

// GET /api/user/profile
router.get("/profile", getProfile);

// PUT /api/user/profile
router.put("/profile", updateProfile);

export default router;
