import os
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="isabelle.db.elephantsql.com",
    database="wgmxepoa",
    user="wgmxepoa",
    password="URKWt_rx7o1HCsjqRONmR9wrB8ep0QI1")

cursor = conn.cursor()
cursor.execute('SELECT * FROM datos')
resultados = cursor.fetchall()

df = pd.DataFrame()
for x in resultados:
    df2 = pd.DataFrame(list(x)).T
    df = pd.concat([df,df2])

df.to_html('web/sqldata.html')