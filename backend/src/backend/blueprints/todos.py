from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import cast

from quart import Blueprint, ResponseReturnValue, g
from quart_auth import current_user, login_required
from quart_rate_limiter import rate_limit
from quart_schema import validate_querystring, validate_request, validate_response

from backend.lib.api_error import APIError
from backend.models.todos import (
    Todo,
    insert_todo,
    select_todo,
    select_todos,
    update_todo,
)

blueprint = Blueprint("todos", __name__)


@dataclass
class TodoData:
    complete: bool
    due: datetime | None
    task: str


@dataclass
class Todos:
    todos: list[Todo]


@dataclass
class TodoFilter:
    complete: bool | None = None


@blueprint.post("/todos/")
@login_required
@rate_limit(10, timedelta(minutes=1))
@validate_request(TodoData)
@validate_response(Todo, 1)
async def create_todos(data: TodoData) -> tuple[Todo, int]:
    todo = await insert_todo(
        data.task,
        data.complete,
        data.due,
        int(cast(str, current_user.auth_id)),
        g.connection,
    )
    return todo, 201


@blueprint.get("/todos/<int:id>/")
@login_required
@rate_limit(10, timedelta(seconds=10))
@validate_response(Todo)
async def get_todo_by_id(id: int) -> Todo:
    todo = await select_todo(id, int(cast(str, current_user.auth_id)), g.connection)
    if todo is None:
        raise APIError(404, "NOT FOUND")
    else:
        return todo


@blueprint.get("/todos/")
@rate_limit(10, timedelta(seconds=10))
@login_required
@validate_response(Todos)
@validate_querystring(TodoFilter)
async def get_todos(queryArgs: TodoFilter) -> Todos:
    todos = await select_todos(
        int(cast(str, current_user.auth_id)),
        queryArgs.complete,
        g.connection,
    )
    return Todos(todos)


@blueprint.put("/todos/<int:id>/")
@login_required
@rate_limit(10, timedelta(seconds=10))
@validate_request(TodoData)
@validate_response(Todo)
async def put_todo(id: int, data: TodoData) -> Todo:
    todo = await update_todo(
        id,
        int(cast(str, current_user.auth_id)),
        data.due,
        data.complete,
        data.task,
        g.connection,
    )
    if todo is None:
        raise APIError(404, "NOT FOUND")
    else:
        return todo


@blueprint.delete("/todos/<int:id>/")
@rate_limit(10, timedelta(seconds=10))
@login_required
async def delete_todo(id: int) -> ResponseReturnValue:
    await delete_todo(
        int(cast(str, current_user.auth_id)),
        id,
        g.connection,
    )
    return "", 202
