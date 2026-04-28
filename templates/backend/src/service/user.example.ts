// Example User Service
// import User from '../model/user.example.js';

export const getById = async (id: string) => {
  // return await User.findByPk(id);
  return { id, name: "Example User" }; // Placeholder
};

export const create = async (data: Record<string, unknown>) => {
  // return await User.create(data);
  return { id: "uuid", ...data }; // Placeholder
};

export const update = async (id: string, data: Record<string, unknown>) => {
  // const user = await User.findByPk(id);
  // return await user.update(data);
  return { id, ...data }; // Placeholder
};

export const remove = async (id: string) => {
  // const user = await User.findByPk(id);
  // return await user.destroy();
  return true; // Placeholder
};
