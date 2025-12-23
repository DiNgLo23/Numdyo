import sqlite3
import time


def create_table_users():
    con = sqlite3.connect("../../data/NumDuo.db")
    con.execute("""CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username STRING,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        points INTEGER,
                        level INTEGER,
                        createAt INTEGER,
                        updateAt INTEGER)
            """)
    con.close()




def create_table_problems():
    con = sqlite3.connect("../../data/NumDuo.db")
    con.execute("""CREATE TABLE IF NOT EXISTS Problems (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT,
                        answer TEXT,
                        level INTEGER,
                        points INTEGER)
            """)
    con.close()




def create_table_problems_with_variants():
    con = sqlite3.connect("../../data/NumDuo.db")
    con.execute("""CREATE TABLE IF NOT EXISTS Problems_with_variants (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        level TEXT,
                        text TEXT,
                        answer_a TEXT,
                        answer_b TEXT,
                        answer_c TEXT,
                        answer_d TEXT,
                        answer_true TEXT
                        )
            """)
    con.close()



create_table_problems_with_variants()

def create_table_achievement():
    con = sqlite3.connect("../../data/NumDuo.db")
    con.execute("""CREATE TABLE IF NOT EXISTS achievement (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        description TEXT,
                        picture TEXT)
            """)
    con.close()




create_table_problems()
create_table_achievement()
create_table_users()