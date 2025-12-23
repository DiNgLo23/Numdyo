import sqlite3
import pandas as pd


df = pd.read_excel('')


con = sqlite3.connect('')
cur = con.cursor()


for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO Problems_with_variants (title, level, text, answer_a, answer_b, answer_c, answer_d, answer_true)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(row['Тема']),
        str(row['Уровень']),
        str(row['Задача']),
        str(row['Вариант A']),
        str(row['Вариант B']),
        str(row['Вариант C']),
        str(row['Вариант D']),
        str(row['Правильный ответ'])
    ))

con.commit()
con.close()
