from fastapi import FastAPI
import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname="sistema_recargas_viajes",
            user="admin",
            password="Pass!__2025!",
            host="149.130.169.172",
            port="33333"
        )
        return connection
    except Exception as e:
        print(f"Error: {e}")

app = FastAPI()

@app.get("/users/count")
def count():
    conn = get_connection()
    cursor = conn.cursor()
    print(cursor.execute("select count(*) from usuarios;"))
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_users":total}

@app.get("/users/active/count")
def count_active_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM usuarios u
        INNER JOIN tarjetas t ON u.usuario_id = t.usuario_id
        WHERE t.estado = 'Activa'
    """)
    total2 = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"users_active_count": total2}

@app.get("/users/latest")
def latest_user():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT CONCAT(nombre, ' ', apellido) AS full_name
        FROM usuarios
        ORDER BY fecha_registro DESC
        LIMIT 1;
    """)
    total3 = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"latest_user": total3}


@app.get("/trips/total")
def count():
    conn = get_connection()
    cursor = conn.cursor()
    print(cursor.execute("SELECT COUNT(*) AS total_trips FROM VIAJES;"))
    total4 = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_trips":total4}

@app.get("/finance/revenue")
def count():
    conn = get_connection()
    cursor = conn.cursor()
    print(cursor.execute("SELECT SUM(t.valor) AS total_revenue, 'COP' AS currency FROM VIAJES v JOIN TARIFAS t ON v.tarifa_id = t.tarifa_id;"))
    total5 = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"total_revenue":total5}
