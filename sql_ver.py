import csv
import os
import zipfile

import asyncpg
from asyncpg.exceptions import UniqueViolationError

from utilites import csv_reader

CSV_SELECT = {
    "users.csv": 'SELECT * FROM users;',
    "addresses.csv": 'SELECT * FROM addresses;',
    "users_roles.csv": 'SELECT * FROM users_roles;',
    "orders.csv": 'SELECT * FROM orders;',
}
FIELDNAMES = {
    "users.csv": ['id', 'first_name', 'last_name'],
    "addresses.csv": ['id', 'country', 'city', 'street', 'building', 'user_id'],
    "users_roles.csv": ['id', 'role_type', 'user_id'],
    "orders.csv": ['id', 'status', 'total', 'user_id'],
}
CSV_INSERT = {
    "users.csv": 'INSERT INTO users (id, first_name, last_name) VALUES ($1, $2, $3);',
    "addresses.csv": 'INSERT INTO addresses (id, country, city, street, building, user_id) VALUES ($1, $2, $3, $4, $5, $6);',
    "users_roles.csv": 'INSERT INTO users_roles (id, role_type, user_id) VALUES ($1, $2, $3);',
    "orders.csv": 'INSERT INTO orders (id, status, total, user_id) VALUES ($1, $2, $3, $4);',
}
SQL_CLEAR_TABLES = 'TRUNCATE users CASCADE; TRUNCATE addresses; TRUNCATE users_roles; TRUNCATE orders;'
INT_FIELDS = ['id', 'user_id', 'role_type', 'status', 'total']

def transform(line) -> dict:
    """ Convert values in line from file to corresponding types in DB table. """
    for k in line.keys():
        if k in INT_FIELDS:
            line[k] = int(line[k])
    return line


async def do_sql_import(path: str, delete_file: bool):
    dburl = os.environ['DATABASE_URL_SQL']
    conn = await asyncpg.connect(dsn=dburl)
    async with conn.transaction():
        await conn.execute(SQL_CLEAR_TABLES)
    for filename, sql in CSV_INSERT.items():
        async with conn.transaction():
            for row in csv_reader(path / filename):
                try:
                    row = transform(row)
                    record = list(row.values())
                    await conn.execute(sql, *record)
                except UniqueViolationError:
                    print(f'A duplicate record already exists - {record})')
        print(f'File {path / filename} was successfully imported.')
        if delete_file:
            os.remove(path / filename)
            print(f'File {path / filename} was deleted.')
    await conn.close()


async def do_sql_export(path: str, zip_files: bool):
    dburl = os.environ['DATABASE_URL_SQL']
    conn = await asyncpg.connect(dsn=dburl)
    for filename, sql in CSV_SELECT.items():
        with open(path / filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(FIELDNAMES[filename])
            async with conn.transaction():
                async for record in conn.cursor(sql):
                    writer.writerow(record)
        print(f'Export successful into file {filename}')
    if zip_files:
        with zipfile.ZipFile(path / "db.zip", mode="w") as archive:
            for filename, _ in CSV_SELECT.items():
                archive.write(filename, arcname=filename)
        print('Zip file db.zip created')
