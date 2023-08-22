 
 
# install mysql on your computer
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python 



# import mysql.connector

# dataBase=mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='hemanth6@mYsql',
    

# )

# # prepare a cursor object

# cursorObject=dataBase.cursor()

# # create a database
# cursorObject.execute("CREATE DATABASE elderco")
# print("All Done")




import pymysql


dataBase = pymysql.connect(
    host='localhost',
    user='root',
    password='hemanth6@mYsql'
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# create a database
cursorObject.execute("CREATE DATABASE ecommerce2")
print("All Done")
