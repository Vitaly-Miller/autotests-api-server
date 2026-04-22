# qa-automation-engineer-api-course

## Install requirements

```shell
pip install -r requirements.txt
```

## Create `.env` file

To get started with the project, you need to create a `.env` file in the root of the project directory. This file will
store sensitive environment variables such as database credentials and JWT settings.

### Step-by-Step Guide:

#### 1. Create a .env File:

In your project root directory, create a file named .env.

```shell
touch .env
```

#### 2. Add the Required Variables:

Copy and paste the following environment variables into the `.env` file:

```shell
APP_HOST="http://localhost:8000"

DATABASE_URL="sqlite+aiosqlite:///./local.db"

JWT_ALGORITHM="HS256"
JWT_SECRET_KEY="qa-automation-engineer-api-course-secret-key"
JWT_ACCESS_TOKEN_EXPIRE=1800
JWT_REFRESH_TOKEN_EXPIRE=5184000
```

## Run server

```shell
uvicorn main:app --reload
```