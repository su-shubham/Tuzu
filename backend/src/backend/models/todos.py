from dataclasses import dataclass
from datetime import datetime
from pydantic import constr
from quart_db import Connection

@dataclass
class Todo:
    id:int
    complete: bool
    due: datetime | None
    task : constr(strip_whitespace=True,min_length=1)


async def select_todos(
        connection:Connection,
        member_id:int,
        complete : bool | None = None,
) -> list[Todo]:
    if complete is None:
        query = '''
                SELECT id,complete,due,task FROM todos WHERE member_id=:member_id    
                '''
        values={"member_id":member_id}
    else:
        query = '''
                SELECT id,complete,due,task from todos WHERE member_id=:member_id AND complete=:complete 
                '''
        values={"member_id":member_id,"complete":complete}
    return [Todo(**row) async for row in connection.iterate(query,values)]

async def select_todo(
        id:int,
        member_id:int,
        connection:Connection,
) -> Todo | None:
    result = await connection.fetch_one(
        '''
        SELECT id,complete,due,task FROM todos WHERE id=:id AND member_id=:member_id
        ''',
    values={"member_id":member_id,"id":id}
    )
    return None if result is None else Todo(**result)

async def insert_todo(
        task:str ,
        complete:bool,
        due:datetime | None,
        member_id:int,
        connection:Connection
) -> Todo | None:
    result = await connection.fetch_one(
        '''
        INSERT INTO todos(task,complete,due,member_id) VALUES (:task,:complete,:due,:member_id) 
        RETURNING id,complete,due,task
        ''',
        {"task":task,"due":due,"member_id":member_id,"complete":complete},
    )
    return Todo(**result)

async def update_todo(
        id:int,
        member_id:int,
        due:datetime | None,
        complete:bool,
        task:str,
        connection:Connection
) -> Todo | None:
    result =await connection.fetch_one(
        '''
            UPDATE todos 
                SET complete=:complete,due=:due,task=:task
            WHERE id=:id AND member_id=:member_id
            RETURNING id,complete,task,due
            ''',
        {
            "id":id,
            "complete":complete,
            "task":task,
            "member_id":member_id,
            "due":due,
        },
    )
    return None if result is None else Todo(**result)

async def delete_todo(
        member_id:int,
        id:int,
        connection:Connection
) ->None:
    await connection.execute(
        '''
        DELETE FROM todos WHERE id=:id AND member_id=:member_id
        ''',
        {
            "member_id":member_id,
            "id":id
        }
    )
    
    

    