# blog-management-fastapi
Secure Blog Management API using FastAPI, MySQL, JWT, RBAC
# Blog Management API (FastAPI)

## 🚀 Features
- JWT Authentication (Access + Refresh)
- Role-Based Access Control (Admin, Author, User)
- Blog CRUD operations
- Comments system
- Audit logging
- Pagination, search, filtering

## 🛠 Tech Stack
- FastAPI
- MySQL
- SQLAlchemy
- JWT Auth

## 🔐 Roles
- Admin → Manage users, delete any blog, view logs
- Author → Manage own blogs
- User → View blogs

## 📦 Setup

```bash
git clone <repo_url>
cd blog_management
pip install -r requirements.txt
uvicorn app.main:app --reload

## 📸 Screenshots

See `/screenshots` folder for:
- Swagger
- Postman
- Database
- ER Diagram

