# import os
# from subprocess import call
# from urllib.parse import urlparse
# from quart_auth import QuartAuth
# from quart_db import QuartDB

# # from quart_schema import QuartSchema
# from quart_rate_limiter import RateLimitExceeded, rate_exempt
# from backend.blueprints.control import blueprint as control_blueprint
# from backend.lib.api_error import APIError
# from quart import Quart, ResponseReturnValue

# # from quart_schema import SchemaValidationError

# app = Quart(__name__)
# app.config.from_prefixed_env(prefix="TOZO")
# auth = QuartAuth(app)
# quart_db = QuartDB(app)
# # QuartSchema(app)
# app.register_blueprint(control_blueprint)


# @app.errorhandler(APIError)  # type: ignores
# async def handle_api_error(e: APIError) -> ResponseReturnValue:
#     return {"message": e.message}, e.status_code


# @app.errorhandler(Exception)
# async def handle_generic_error(e: Exception) -> ResponseReturnValue:
#     return {"code": "INTERNAL SERVER ERROR"}, 500


# @app.errorhandler(RateLimitExceeded)
# async def handle_rate_limit_exceeded(e: RateLimitExceeded) -> ResponseReturnValue:
#     return {}, e.get_headers(), 429


# # @app.errorhandler(SchemaValidationError)
# # async def handle_schema_validation(e: SchemaValidationError) -> SchemaValidationError:
# #     if isinstance(e.validation_error, TypeError):
# #         return {"errors": str(e.validation_error)}, 400
# #     else:
# #         return {"errors": e.validation_error.json()}, 400


# @app.cli.command("recreate_db")
# def recreate_db() -> None:
#     db_url = urlparse(os.environ["TOZO_QUART_DB_DATABASE_URL"])
#     call(  # nosec
#         [
#             "psql",
#             "-U",
#             "postgres",
#             "-c",
#             f"DROP DATABASE IF sEXISTS {db_url.path.removeprefix('/')}",
#         ],
#     )
#     call(  # nosec
#         ["psql", "-U", "postgres", "-c", f"DROP USER IF EXISTS {db_url.username}"],
#     )
#     call(  # nosec
#         [
#             "psql",
#             "-U",
#             "postgres",
#             "-c",
#             f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB",
#         ],
#     )
#     call(  # nosec
#         [
#             "psql",
#             "-U",
#             "postgres",
#             "-c",
#             f"CREATE DATABASE {db_url.path.removeprefix('/')}",
#         ],
#     )


# @app.get("/")
# @rate_exempt
# async def ping() -> ResponseReturnValue:
#     return {"ping": "po"}

import logging
import os
from subprocess import call  # nosec
from urllib.parse import urlparse

from quart import Quart, Response, ResponseReturnValue
from quart_auth import QuartAuth
from quart_db import QuartDB
from quart_rate_limiter import RateLimiter, RateLimitExceeded
# from quart_schema import QuartSchema, RequestSchemaValidationError
from werkzeug.http import COOP

from backend.blueprints.control import blueprint as control_blueprint
from backend.lib.api_error import APIError

logging.basicConfig(level=logging.INFO)

app = Quart(__name__)
app.config.from_prefixed_env(prefix="TOZO")

auth_manager = QuartAuth(app)
quart_db = QuartDB(app)
rate_limiter = RateLimiter(app)
# schema = QuartSchema(app, convert_casing=True)

app.register_blueprint(control_blueprint)



@app.errorhandler(APIError)  # type: ignore
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    return {"code": error.code}, error.status_code


@app.errorhandler(500)
async def handle_generic_error(error: Exception) -> ResponseReturnValue:
    return {"code": "INTERNAL_SERVER_ERROR"}, 500


@app.errorhandler(RateLimitExceeded)  # type: ignore
async def handle_rate_limit_exceeded_error(
    error: RateLimitExceeded,
) -> ResponseReturnValue:
    return {}, error.get_headers(), 429


# @app.errorhandler(RequestSchemaValidationError)  # type: ignore
# async def handle_request_validation_error(
#     error: RequestSchemaValidationError,
# ) -> ResponseReturnValue:
#     if isinstance(error.validation_error, TypeError):
#         return {"errors": str(error.validation_error)}, 400
#     else:
#         return {"errors": error.validation_error.json()}, 400


@app.cli.command("recreate_db")
def recreate_db() -> None:
    db_url = urlparse(os.environ["TOZO_QUART_DB_DATABASE_URL"])
    call(  # nosec
        [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"DROP DATABASE IF EXISTS {db_url.path.removeprefix('/')}",
        ],
    )
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"DROP USER IF EXISTS {db_url.username}"],
    )
    call(  # nosec
        [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB",  # noqa: E501
        ],
    )
    call(  # nosec
        [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"CREATE DATABASE {db_url.path.removeprefix('/')}",
        ],
    )


