CLI for user bulk-upload/migration:
1) Build an asynchronous CLI Tool which is easily extendable and unit-testable.
2) All columns can be freely chosen. (e.g. id, first_name, last_name, gender, dob)
3) Tables given: users, addresses, users_roles, orders (please create not less than 3 tables in relation to users table, 4 tables in total is a minimum)
4) Ability to export users with all his relations from a database into csv files.
5) Ability to import users from csv files into an empty database.
6) Ability to import users from csv files into a database containing existing relations [bonus].
7) You are free to decide how database data is stored into csv files.
8) Add the ability to zip exported csv files.
9) After successful import please remove existing csv/zip files.
10) Write tests to cover all added logic, preferably use mocks for db connection.
11) It is essential to demonstrate the use of both ORM and raw SQL.
12) Project description/documentation in the form of: README.md
13) Project dependencies in the form of: requirements.txt
14) Provide code comments, docstrings and typing annotations [bonus].  
15) Ensure your project is functional - this is obvious