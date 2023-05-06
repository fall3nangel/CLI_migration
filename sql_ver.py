
import os

import asyncpg


async def do_sql_import(path: str):
    pass



async def do_sql_export(path: str):
    dburl = os.environ['DATABASE_URL_SQL']
    con = await asyncpg.connect(dsn=dburl)
    result = await con.copy_from_query(
        'SELECT * FROM users', output=path, format='csv')
    print(result)
