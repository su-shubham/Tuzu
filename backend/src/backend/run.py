import logging
import os
import subprocess  # nosec
from urllib.parse import urlparse

from quart import Quart, ResponseReturnValue
from quart_auth import AuthManager
from quart_db import QuartDB
from quart_rate_limiter import RateLimitExceeded
from quart_schema import QuartSchema, SchemaValidationError

from backend.blueprints.control import blueprint as control_blueprint
from backend.blueprints.members import blueprint as member_blueprint
from backend.blueprints.session import blueprint as session_blueprint
from backend.blueprints.todos import blueprint as todo_blueprint

# from backend.lib.api_error import APIError

logging = logging.basicConfig(level=logging.INFO)

app = Quart(__name__)
app.config.from_prefixed_env(prefix="TOZO")
auth_manager = AuthManager(app)
quart_db = QuartDB(app)
QuartSchema(app)
app.register_blueprint(control_blueprint)
app.register_blueprint(session_blueprint)
app.register_blueprint(member_blueprint)
app.register_blueprint(todo_blueprint)


# @app.errorhandler(APIError)  # type: ignores
# async def handle_api_error(e: APIError) -> ResponseReturnValue:
#     return {"message": e.code}, e.status_code


# @app.errorhandler(Exception)
# async def handle_generic_error(e: Exception) -> ResponseReturnValue:
#     return {"code": "INTERNAL SERVER ERROR"}, 500


@app.errorhandler(RateLimitExceeded)
async def handle_rate_limit_exceeded(e: RateLimitExceeded) -> ResponseReturnValue:
    return {}, e.get_headers(), 429


@app.errorhandler(SchemaValidationError)
async def handle_schema_validation(e: SchemaValidationError) -> SchemaValidationError:
    if isinstance(e.validation_error, TypeError):
        return {"errors": str(e.validation_error)}, 400
    else:
        return {"errors": e.validation_error.json()}, 400


@app.cli.command("recreate_db")
def recreate_db() -> None:
    db_url = urlparse(os.environ["TOZO_QUART_DB_DATABASE_URL"])
    psql_path = (
        r"C:\Program Files\PostgreSQL\15\bin\psql.exe"  # Use the correct path to psql
    )

    subprocess.run(
        [
            psql_path,
            "-U",
            "postgres",
            "-c",
            f"DROP DATABASE IF EXISTS {db_url.path.removeprefix('/')}",
        ],
        shell=True,  # nosec
    )

    subprocess.run(
        [
            psql_path,
            "-U",
            "postgres",
            "-c",
            f"DROP USER IF EXISTS {db_url.username}",
        ],
        shell=True,  # nosec
    )

    subprocess.run(
        [
            psql_path,
            "-U",
            "postgres",
            "-c",
            f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB",
        ],
        shell=True,  # nosec
    )  # noqa: E501

    subprocess.run(
        [
            psql_path,
            "-U",
            "postgres",
            "-c",
            f"CREATE DATABASE {db_url.path.removeprefix('/')}",
        ],
        shell=True,  # nosec
    )


@app.get("/")
async def main():
    return {"hello": "pong"}
