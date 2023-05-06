import csv
import os
import zipfile

from sqlalchemy import inspect, select

from db import Model, Session, engine
from models import Address, Order, User, UserRole


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


async def do_orm_import(path: str):
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all)  # warning: this deletes all data!
        await connection.run_sync(Model.metadata.create_all)
    async with Session() as session:
        async with session.begin():
            with open(path) as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    role_type = row.pop('role_type')
                    role = UserRole(role_type=int(role_type))
                    user_name = row.pop('first_name')
                    user_l_name = row.pop('last_name')
                    addr = Address(**row)
                    user = User(first_name=user_name, last_name=user_l_name)
                    session.add(user)
                    user.users_roles.append(role)
                    user.addresses.append(addr)
    os.remove(path)  # not async - replace to aiofiles
    print('Import successful')


async def do_orm_export(path: str):
    async with Session() as session:
        async with session.begin():
            with open(path, 'w', newline='') as f:
                fieldnames = list([column.name for column in User.__table__.columns])
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                query = select(User)
                res = await session.stream(query)
                async for row in res:
                    dct = object_as_dict(row[0])
                    writer.writerow(dct)
    print('Export successful')
    with zipfile.ZipFile("test.zip", mode="w") as archive:
        archive.write(path)
    print('Zip file created')
