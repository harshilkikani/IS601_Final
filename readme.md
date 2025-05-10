# User Management System Final Project

This project is a robust User Management System built for IS601, featuring:
- User profile management (view, update, secure fields)
- Role-Based Access Control (RBAC) for admin and regular users
- Professional status upgrade workflow
- Secure authentication and validation
- Notification system for key user actions
- Comprehensive API test coverage

## Quick Start

### 1. Clone the Repository
```
git clone https://github.com/harshilkikani/IS601_Final.git
cd IS601_Final
```

### 2. Run with Docker Compose
```
docker-compose up --build
```

### 3. Run Tests
```
docker exec <fastapi_container_name> pytest
```

## DockerHub Image
- Pull the latest image:
  ```
  docker pull hk453/is601_final:latest
  ```
- [View on DockerHub](https://hub.docker.com/r/hk453/is601_final)

## Repository Structure
- `app/` - FastAPI application code
- `tests/` - Test suite (pytest)
- `Project Instructions/` - Project documentation and requirements