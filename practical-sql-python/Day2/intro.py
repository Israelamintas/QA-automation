from mysql.connector import connect

# mysql://root:WzdtUoxoaGhIAmlyTTNoyPejxJhgtEar@altaria.proxy.rlwy.net:47337/railway

connection = connect(
    host="altaria.proxy.rlwy.net",
    port="47337",
    user="root",
    password="WzdtUoxoaGhIAmlyTTNoyPejxJhgtEar",
    database="railway",
    charset="utf8mb4",
)

print("Conectado:", connection.is_connected())

# cursor = connection.cursor()
# cursor.execute("SELECT 1;")
# print("Teste SELECT 1:", cursor.fetchone())

# connection.close()
