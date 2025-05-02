import socket

HOST = '0.0.0.0'
PORT = 631

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ECO] Servidor escuchando en puerto {PORT}")

    while True:
        conn, addr = server.accept()
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

