import asyncio
from argparse import ArgumentParser
from orm_ver import do_orm_import, do_orm_export


async def main():
    parser = ArgumentParser(description='Upload and download content of User database')
    parser.add_argument('-oi', '--do_orm_import', action='store_true', help='Import content of CSV file to Users DB using ORM')
    parser.add_argument('-oe', '--do_orm_export', action='store_true', help='Export content of Users DB to CSV file using ORM')
    parser.add_argument('path')
    args = parser.parse_args()
    if args.do_orm_import:
        await do_orm_import(args.path)
    elif args.do_orm_export:
        await do_orm_export(args.path)


if __name__ == '__main__':
    asyncio.run(main())
