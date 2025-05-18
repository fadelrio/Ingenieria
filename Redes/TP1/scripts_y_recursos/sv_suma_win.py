import socket

HOST = '0.0.0.0'
PORT = 5000  # Puerto de escucha para SUMA

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[SUMA] Servidor escuchando en puerto {PORT}...")

    while True:
        conn, addr = s.accept()
        print(f"[SUMA] Conexión aceptada desde {addr}")
        with conn:
            while True:
                try:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break
                    if data.startswith("/suma "):
                        try:
                            _, num1, num2 = data.split()
                            resultado = float(num1) + float(num2)
                            response = f"{num1} + {num2} = {resultado}\n"
                            conn.sendall(response.encode())
                        except:
                            conn.sendall(b"Error en los argumentos. Cerrando conexion.\n")
                            break
                    else:
                        print(f"[SUMA] Comando inválido: {data}")
                        conn.sendall(b"Comando invalido. Cerrando conexion.\n")
                        break
                except ConnectionResetError:
                    break
        print("[SUMA] Conexión cerrada.")
