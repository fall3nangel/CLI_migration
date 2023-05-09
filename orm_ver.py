import os
import zipfile

from sqlalchemy import exc, inspect, select

from db import Model, Session, engine
from models import Address, Order, User, UserRole
from utilites import csv_reader

CSV_TABLES = {
    "users.csv": User,
    "addresses.csv": Address,
    "users_roles.csv": UserRole,
    "orders.csv": Order,
}

def object_as_dict(obj) -> dict:
    """ Convert DB table record to dict. """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def transform(line, table) -> dict:
    """ Convert values in line from file to corresponding types in DB table. """
    for k in line.keys():
        col = inspect(table).columns[k]
        if col.type.python_type is int:
            line[k] = int(line[k])
    return line


async def do_orm_import(path: str, delete_file: bool):
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all)  # warning: this deletes all data!
        await connection.run_sync(Model.metadata.create_all)
    async with Session() as session:
        for filename, table in CSV_TABLES.items():
            if os.path.exists(path / filename):
                try:
                    async with session.begin():
                        for row in csv_reader(path / filename):
                            row = transform(row, table)
                            record = table(**row)
                            session.add(record)
                except ValueError:
                    print("Value Error")
                except exc.SQLAlchemyError as e:
                    print(f"Error in import - {e}")
                else:
                    print(f'File {path / filename} was successfully imported.')
                    if delete_file:
                        os.remove(path / filename)
                        print(f'File {path / filename} was deleted.')

            else:
                print(f'File {path / filename} not found.')
    return True


async def do_orm_export(path: str, zip_files: bool):
    async with Session() as session:
        async with session.begin():
            for filename, table in CSV_TABLES.items():
                with open(path / filename, 'w', newline='') as f:
                    fieldnames = list([column.name for column in table.__table__.columns])
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                    writer.writeheader()
                    query = select(table)
                    res = await session.stream(query)
                    async for row in res:
                        dct = object_as_dict(row[0])
                        writer.writerow(dct)
                print(f'Export successful into file {filename}')
    if zip_files:
        with zipfile.ZipFile(path / "db.zip", mode="w") as archive:
            for filename, _ in CSV_TABLES.items():
                archive.write(filename, arcname=filename)
        print('Zip file db.zip created')
