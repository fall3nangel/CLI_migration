
Usage
- ```docker-compose up -d``` Run Postgree
- ``` mv .env.example .env``` Rename .env.example to .env
- ```pip install -r requirements.txt``` Install dependencies
- ```python3 cli.py -oi ./sample_data/``` Import content of CSV files from sample_data directory to Users DB using ORM
- ```python3 cli.py -oe ``` Export content of Users DB to CSV files in current directory using ORM
- ```python3 cli.py -si ./sample_data/``` Import content of CSV file from sample_data directory to Users DB using SQL
- ```python3 cli.py -se``` Export content of Users DB to CSV files in current directory using SQL
 
