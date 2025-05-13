import sqlite3


def clear_database(file_path):
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        cursor.execute(f"DELETE FROM {table[0]};")
    connection.commit()
    connection.close()

file_path = 'laptops.db'


clear_database(file_path)
