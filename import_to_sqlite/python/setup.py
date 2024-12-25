import csv
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

# Reading and inserting CSV data
with open('file.csv', 'r') as file:
    csv_data = csv.reader(file)
    next(csv_data)  # Skip the header row
    for row in csv_data:
        cursor.execute(
            "INSERT INTO your_table_name (column1, column2, column3) VALUES (%s, %s, %s)",
            row
        )
conn.commit()
cursor.close()
conn.close()
