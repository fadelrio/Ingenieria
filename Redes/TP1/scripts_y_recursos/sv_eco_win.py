import socket

HOST = '0.0.0.0'
PORT = 5001  # Puerto de escucha para ECO

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[ECO] Servidor escuchando en puerto {PORT}...")

    while True:
        conn, addr = s.accept()
        print(f"[ECO] Conexión aceptada desde {addr}")
        with conn:
            while True:
                try:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break
                    if data.startswith("/eco "):
                        response = data[5:] + "\n"
                        conn.sendall(response.encode())
                    else:
                        print(f"[ECO] Comando inválido: {data}")
                        conn.sendall(b"Comando invalido. Cerrando conexion.\n")
                        break
                except ConnectionResetError:
                    break
        print("[ECO] Conexión cerrada.")