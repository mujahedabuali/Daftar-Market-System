import mysql.connector
import hashlib

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MmM002003@",
    database="mukhmasi"
)

mycursor = mydb.cursor()


