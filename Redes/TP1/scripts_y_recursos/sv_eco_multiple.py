import socket
import threading

HOST = '0.0.0.0'
PORT = 5000
MAX_CONEXIONES = 2

def manejar_cliente(conn, addr):
    print(f"[ECO] Conexión desde {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            if data.startswith("/eco"):
                texto = data[5:]
                conn.sendall(f"{texto}\n".encode())
            else:
                conn.sendall(b"Comando no reconocido. Cerrando conexion.\n")
                break
    print(f"[ECO] Conexión cerrada {addr}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(MAX_CONEXIONES)  # Permite 2 conexiones en cola
    print(f"[ECO] Servidor escuchando en puerto {PORT}")

    while True:
        conn, addr = server.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
        hilo.start()

