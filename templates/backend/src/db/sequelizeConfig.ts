import { Sequelize } from "sequelize";
import dotenv from "dotenv";
import logger from "../utility/logger.js";

dotenv.config();

const sequelize = new Sequelize(
  `postgresql://${process.env.DB_USER}:${process.env.DB_PASSWORD}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_TABLE}`,
  {
    dialect: "postgres",
    dialectOptions: {
      ssl:
        process.env.NODE_ENV === "production"
          ? { require: true, rejectUnauthorized: false }
          : false
    },
    logging: false
  }
);

export default sequelize;

export const db = async (): Promise<number> => {
  try {
    await sequelize.authenticate();
    logger.info("Sequelize connected successfully");
    return 1;
  } catch (error: any) {
    logger.error("Sequelize connected failed:", error.message);
    process.exit(1);
  }
};
