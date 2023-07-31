from quart_db import Connection

async def execute(connection:Connection) -> None:
    await connection.execute(
        '''
        INSERT INTO members(email,password_hash) VALUES("shubham@tozo.co","systemctl restart postgresql@14-main.service")
        '''
    )
    await connection.execute(
        '''
            INSERT INTO todos(task,member_id) VALUES("TEST TASK 1",1)
        '''
    )