// Example User Controller
import { Request, Response } from "express";
import response from "../utility/response.js";
import { HTTP_STATUS_CODE } from "../utility/httpStatusCode.js";
// import User from '../model/user.example.js';

// Get current user profile
export const getProfile = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.userId;

    // Example: fetch user from database
    // const user = await User.findByPk(userId);

    // Placeholder response
    const user = {
      id: userId,
      email: (req as any).user.email,
      name: (req as any).user.name
    };

    return response(res, HTTP_STATUS_CODE.OK, user);
  } catch (error) {
    console.error("Error fetching profile:", error);
    return response(res, HTTP_STATUS_CODE.INTERNAL_SERVER_ERROR, "Failed to fetch profile");
  }
};

// Update user profile
export const updateProfile = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.userId;
    const { name, avatarUrl } = req.body;

    // Example: update user in database
    // const user = await User.findByPk(userId);
    // await user.update({ name, avatarUrl });

    return response(res, HTTP_STATUS_CODE.OK, { message: "Profile updated successfully" });
  } catch (error) {
    console.error("Error updating profile:", error);
    return response(res, HTTP_STATUS_CODE.INTERNAL_SERVER_ERROR, "Failed to update profile");
  }
};

export default {
  getProfile,
  updateProfile
};
