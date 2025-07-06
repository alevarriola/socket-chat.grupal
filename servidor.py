import socket
import sys


# Crear socket TCP (stream) para IPv4
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permitir reusar la dirección si reiniciás rápido
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Validar argumentos
if len(sys.argv) != 3:
    print("Uso: python servidor.py <IP> <PUERTO>")
    sys.exit(1)

IP = str(sys.argv[1])     # IP desde línea de comandos
PUERTO = int(sys.argv[2]) # Puerto desde línea de comandos

servidor.bind((IP, PUERTO))
servidor.listen(10)

print(f"Servidor escuchando en {IP}:{PUERTO}")

# Lista de sockets activos (servidor + clientes)
sockets_activos = [servidor]