import socket

HOST = '0.0.0.0'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SUMA] Servidor escuchando en puerto {PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[SUMA] Conexión desde {addr}")
        with conn:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                if data.startswith("/suma"):
                    try:
                        _, a, b = data.split()
                        resultado = float(a) + float(b)
                        conn.sendall(f"{a} + {b} = {resultado}\n".encode())
                    except Exception:
                        conn.sendall(b"Error: Comando invalido\n")
                        break
                else:
                    conn.sendall(b"Comando no reconocido. Cerrando conexion.\n")
                    break

