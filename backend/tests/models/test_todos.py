import pytest
from quart_db import Connection

from backend.models.todos import delete_todo, insert_todo, select_todo, update_todo


@pytest.mark.parametrize("member_id,deleted", [(1, True), (2, False)])
async def test_delete_todo(
    connection: Connection, member_id: int, deleted: bool
) -> None:
    todo = await insert_todo("Task", False, None, 1, connection)
    await delete_todo(member_id, todo.id, connection)
    result = await select_todo(todo.id, 1, connection)
    assert (result is None) is deleted


@pytest.mark.parametrize("member_id,completed", [(1, True), (2, False)])
async def test_update_todo(
    connection: Connection, member_id: int, completed: bool
) -> None:
    todo = await insert_todo("Task", False, None, 1, connection)
    await update_todo(todo.id, member_id, None, True, "Task", connection)
    new_todo = await select_todo(todo.id, 1, connection)
    assert new_todo is not None
    assert new_todo.complete is completed
