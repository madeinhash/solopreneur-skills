# Backend Template

Express + Sequelize + PostgreSQL backend template

## Directory Structure

```
src/
├── index.js              # App entry point
├── router/               # Route layer: Define API endpoints, dispatch to controllers
├── controller/           # Controller layer: Validate input, call services, return response
├── service/              # Service layer: Business logic implementation
├── model/                # Model layer: Sequelize data model definitions (table schema)
├── db/
│   ├── migrations/       # Database migrations: Schema change records (create tables, add fields)
│   ├── sequelizeConfig.js
│   └── sequelizeConfigCommon.cjs
├── middleware/           # Middleware: JWT auth, request processing
└── utility/              # Utilities: Logger, response formatter, error classes
```

## Layer Responsibilities

| Layer | Responsibility | Example |
|---|---|---|
| **router** | Define API routes, specify HTTP methods and paths | `router.get('/users/:id', getUser)` |
| **controller** | Validate request params, call service, format response | Check if id is valid, call `userService.getById()` |
| **service** | Implement business logic, operate database | Query users, process data, transaction management |
| **model** | Define table structure and relationships | `User.hasMany(Post)` |
| **migrations** | Record database schema changes, version control | Create users table, add email field |

## Request Flow

```
Request → Router → Controller → Service → Model → Database
                                    ↓
Response ← Controller ← Service ←──┘
```

## Getting Started

1. Copy environment variables file
```bash
cp .env.template .env
```

2. Configure database connection and other variables in `.env`

3. Install dependencies
```bash
npm install
```

4. Run database migrations
```bash
npm run db:migrate
```

5. Start development server
```bash
npm run local
```

## Adding New Features Example

Example: Adding Post functionality

### 1. Create Migration
```bash
npx sequelize-cli migration:generate --name create-posts
```
```javascript
// db/migrations/xxxx-create-posts.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('posts', {
      id: { type: Sequelize.UUID, primaryKey: true },
      title: { type: Sequelize.STRING, allowNull: false },
      content: { type: Sequelize.TEXT },
      userId: { type: Sequelize.UUID, references: { model: 'users', key: 'id' } },
      createdAt: Sequelize.DATE,
      updatedAt: Sequelize.DATE,
    });
  },
  down: async (queryInterface) => {
    await queryInterface.dropTable('posts');
  }
};
```

### 2. Create Model
```javascript
// model/post.js
const Post = sequelize.define('Post', {
  id: { type: DataTypes.UUID, primaryKey: true, defaultValue: DataTypes.UUIDV4 },
  title: { type: DataTypes.STRING, allowNull: false },
  content: { type: DataTypes.TEXT },
  userId: { type: DataTypes.UUID },
});
```

### 3. Create Service
```javascript
// service/postService.js
import Post from '../model/post.js';

export const create = async (data) => {
  return await Post.create(data);
};

export const getById = async (id) => {
  return await Post.findByPk(id);
};

export const list = async (userId) => {
  return await Post.findAll({ where: { userId } });
};
```

### 4. Create Controller
```javascript
// controller/postController.js
import * as postService from '../service/postService.js';

export const createPost = async (req, res) => {
  const { title, content } = req.body;

  // Validate input
  if (!title) {
    return response(res, HTTP_STATUS_CODE.BAD_REQUEST, 'Title is required');
  }

  // Call service
  const post = await postService.create({
    title,
    content,
    userId: req.user.userId
  });

  return response(res, HTTP_STATUS_CODE.CREATED, post);
};
```

### 5. Create Router
```javascript
// router/post.js
import express from 'express';
import { createPost, getPost, listPosts } from '../controller/postController.js';
import { checkJWT } from '../middleware/checkJWTMiddleWare.js';

const router = express.Router();
router.use(checkJWT);

router.post('/', createPost);
router.get('/:id', getPost);
router.get('/', listPosts);

export default router;
```

### 6. Register Router
```javascript
// router/index.js
import postRouter from './post.js';
router.use('/posts', postRouter);
```

## Commands

```bash
npm run local      # Local development (hot reload)
npm run dev        # Development environment
npm run build      # Build
npm run start      # Production environment
npm run db:migrate # Run database migrations
```
# backend-template
