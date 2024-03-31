# Development

## Local development setup

### Preparations

Generate secret key for your application.
```bash
openssl rand -hex 32
```

Create `.env` file
```dotenv
SECRET_KEY="my_secret_key_from_previous_step"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
MYSQL_DATABASE="my_db"
MYSQL_USER="my_user"
MYSQL_PASSWORD="my_password"
MYSQL_ROOT_PASSWORD="my_password"
```

Docker version 25.0.3
Docker Compose version v2.24.6-desktop.1

### Create and start docker containers

```powershell
docker-compose up --build
```

Once the container are up and running, it is required to upgrade mysql database to the latest revision.
```powershell
alembic upgrade head
```

Then access http://localhost:8000/docs

### pre-commit
As a helper for linting we use [pre-commit](https://pre-commit.com/)

```powershell
pip install pre-commit
pre-commit install
```

## Tests
Enter docker container
```powershell
docker-compose run -e -it legendary_winner /bin/bash
```

Execute tests locally
```powershell
pytest tests/
```

At the moment there are no tests, just a placeholder for future tests implementation

## Local setup for rendering the docs

One can view the documentation in `docs/` folder as follows
```powershell
pip install --upgrade setuptools
pip install -r reqs/docs-requirements.txt
mkdocs serve
```
Then access http://127.0.0.1:8000/
