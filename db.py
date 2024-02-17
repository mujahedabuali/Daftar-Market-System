import mysql.connector
import hashlib

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@",
    database="mukhmasi"
)

mycursor = mydb.cursor()


