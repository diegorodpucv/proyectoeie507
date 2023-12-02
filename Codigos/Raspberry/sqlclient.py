import time
import serial
import psycopg2
import os
RaspID = '1'

ser = serial.Serial('/dev/ttyACM0',9600)
ser.setDTR(False)
time.sleep(1)
ser.flushInput ()
ser.setDTR(True)

conn = psycopg2.connect(
    host="isabelle.db.elephantsql.com",
    database="wgmxepoa",
    user="wgmxepoa",
    password="URKWt_rx7o1HCsjqRONmR9wrB8ep0QI1")

print("Conectado")
cursor = conn.cursor()

while True:
        dato = ser.readline().decode('utf-8').rstrip('\r\n')
        dato2 = dato.split(",")
        ArdID = dato2[0]
        t = dato2[1]
        h = dato2[2]
        timestamp = time.strftime("\'%Y-%m-%d_%H:%M:%S\'")
        ultradatos = (RaspID,ArdID,t,h,timestamp)
        sql = "INSERT INTO public.datos(rasp_id, arduino_id, temp_value, hum_value, fecha) VALUES (%s,%s,%s,%s,%s)"
        try:
                cursor.execute(sql,(RaspID,ArdID,t,h,timestamp))
                conn.commit()
                print(f"Datos Subidos Correctamente: {ultradatos}")
                time.sleep(900)

        except Exception as e:
                print(f"Error: {e}")

cursor.close()
conn.close()
ser.close()