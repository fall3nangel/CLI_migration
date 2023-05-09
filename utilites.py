import csv

def csv_reader(file_name: str):
    """ Yields the lines of CSV file one by one."""
    try:
        with open(file_name, "r") as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                yield row
    except FileNotFoundError:
        print(f'File {file_name} not found.')