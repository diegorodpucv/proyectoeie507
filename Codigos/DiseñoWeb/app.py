from flask import Flask, render_template, request
import psycopg2
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Configura la conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="isabelle.db.elephantsql.com",
    database="wgmxepoa",
    user="wgmxepoa",
    password="URKWt_rx7o1HCsjqRONmR9wrB8ep0QI1")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafico', methods=['POST'])
def generar_grafico():
    # Obtiene los parámetros del formulario
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    raspi_id = request.form['raspi_id']
    ardu_id = request.form['ardu_id']

    # Consulta a la base de datos para obtener los datos en el rango de fechas
    cursor = conn.cursor()
    query = "SELECT fecha, temp_value, hum_value FROM datos WHERE fecha BETWEEN %s AND %s AND rasp_id = %s AND arduino_id = %s"
    cursor.execute(query, (fecha_inicio, fecha_fin, raspi_id, ardu_id))
    data = cursor.fetchall()
    cursor.close()

    # Genera el gráfico con Matplotlib
    fig, ax = plt.subplots()
    fechas = [item[0] for item in data]
    temp = [item[1] for item in data]
    hum = [item[2] for item in data]

    ax.set_xlabel('Fecha')
    ax.set_ylabel('Temperatura', color='tab:blue')
    ax.plot(fechas, temp, color='tab:blue')
    ax.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax.twinx()
    ax2.set_ylabel('Humedad', color='tab:red')
    ax2.plot(fechas, hum, color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    ax.set_title('Gráfico de Datos Temperatura y Humedad')
    # Convierte el gráfico a una imagen en formato base64
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')
    plt.close()

    # Renderiza la plantilla con la imagen del gráfico
    return render_template('grafico.html', img_str=img_str)

if __name__ == '__main__':
    app.run(debug=True)
