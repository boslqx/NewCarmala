import sqlite3

def connect_database():
    database = sqlite3.connect('carmala.db')
    return database

