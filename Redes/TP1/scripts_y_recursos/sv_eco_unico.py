import socket

HOST = '0.0.0.0'
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)  # Permite 1 conexión pendiente
    print(f"[ECO] Servidor escuchando en puerto {PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[ECO] Conexión aceptada desde {addr}")
        with conn:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    print("[ECO] Cliente desconectado.")
                    break
                if data.startswith("/eco"):
                    texto = data[5:]
                    conn.sendall(f"{texto}\n".encode())
                else:
                    conn.sendall(b"Comando no reconocido. Cerrando conexion.\n")
                    break



