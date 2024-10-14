import sqlite3

# connect to database and create file Carmala
connection = sqlite3.connect('Carmala.db')

# create a cursor to execute SQL commands
cursor = connection.cursor()

# create table User_account
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserAccount (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT NOT NULL,
        Username TEXT NOT NULL,
        Password TEXT NOT NULL,
        ProfilePicture BLOB,
        Gender TEXT,
        Country TEXT,
        DrivingLicense BLOB,
        IdentificationNumber TEXT    
    )
''')

# create table AdminAccount
cursor.execute('''
    CREATE TABLE IF NOT EXISTS AdminAccount (
        Admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Admin_username TEXT NOT NULL,
        Admin_password TEXT NOT NULL,
        Admin_email TEXT NOT NULL,
    )
''')

# create table CARTABLE
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CARTABLE (
        CAR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CAR_NAME TEXT NOT NULL,
        CAR_LOCATION TEXT NOT NULL,
        CAR_CAPACITY TEXT NOT NULL,
        CAR_FUELTYPE TEXT NOT NULL,
        CAR_TRANSMISSION TEXT NOT NULL,
        CAR_FEATURES TEXT NOT NULL,
        CAR_PRICE TEXT NOT NULL,
        CAR_IMAGE TEXT NOT NULL,
        ADMIN_ID INTEGER,
        FOREIGN KEY (Admin_id) REFERENCES AdminAccount(Admin_id) on delete cascade
    )
''')



# commit the changes and close the connection
connection.commit()
connection.close()


