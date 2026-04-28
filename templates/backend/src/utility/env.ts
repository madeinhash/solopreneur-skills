import dotenv from "dotenv";

dotenv.config();

export const isLocalDev = (): boolean => {
  return process.env.NODE_ENV?.trim() === "local" || process.env.NODE_ENV?.trim() === "development";
};

export const isUat = (): boolean => {
  return process.env.NODE_ENV?.trim() === "uat";
};

export const isProd = (): boolean => {
  return process.env.NODE_ENV?.trim() === "production";
};
