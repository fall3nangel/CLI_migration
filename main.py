import csv
import asyncio
import os
import zipfile
from argparse import ArgumentParser

from sqlalchemy import inspect, select

from db import Model, Session, engine
from models import Address, Order, User, UserRole


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


async def do_import(path: str):
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all)  # warning: this deletes all data!
        await connection.run_sync(Model.metadata.create_all)
    async with Session() as session:
        async with session.begin():
            with open(path) as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    role_type = row.pop('role_type')
                    role = UserRole(role_type=role_type)
                    user_name = row.pop('first_name')
                    user_l_name = row.pop('last_name')
                    addr = Address(**row)
                    user = User(first_name=user_name, last_name=user_l_name)
                    session.add(user)
                    user.users_roles.append(role)
                    user.addresses.append(addr)
    os.remove(path)  # not async - replace to aiofiles
    print('Import successful')


async def do_export(path: str):
    async with Session() as session:
        async with session.begin():
            with open(path, 'w', newline='') as f:
                query = select(User)
                fieldnames = list([column.name for column in User.__table__.columns])
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                for row in session.execute(query):
                    dct = object_as_dict(row[0])
                    writer.writerow(dct)
    print('Export successful')
    with zipfile.ZipFile("test.zip", mode="w") as archive:
        archive.write(path)
    print('Zip file created')


async def main():
    parser = ArgumentParser(description='Upload and download content of User database')
    parser.add_argument('-i', '--do_import', action='store_true', help='Import content of CSV file to Users DB')
    parser.add_argument('-e', '--do_export', action='store_true', help='Export content of Users DB to CSV file')
    parser.add_argument('path')
    args = parser.parse_args()
    if args.do_import:
        await do_import(args.path)
    elif args.do_export:
        await do_export(args.path)


if __name__ == '__main__':
    asyncio.run(main())
