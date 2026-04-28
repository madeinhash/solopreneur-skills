const dotenv = require('dotenv');

dotenv.config();

const config = {
  dialect: 'postgres',
  dialectOptions: {
    ssl: process.env.NODE_ENV === 'production' 
      ? { require: true, rejectUnauthorized: false }
      : false
  },
  logging: console.log
};


module.exports = {
  ...config,
  dialect: 'postgres',
  username: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  host: process.env.DB_HOST,
  database: process.env.DB_TABLE,
  port: process.env.DB_PORT,
  logging: false,
  migrationStorageTableName: 'sequelize_migration_record'
};