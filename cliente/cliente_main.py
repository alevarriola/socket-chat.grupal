import socket
import sys
import threading
from cliente_logic import recibir_mensajes, enviar_mensajes

if len(sys.argv) != 3:
    print("Uso: python cliente.py <IP> <PUERTO>")
    sys.exit(1)

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# tratamos de conectarnos al servidor, si falla terminar programa
try:
    cliente_socket.connect((IP, PUERTO))
    print(f"Conectado al servidor {IP}:{PUERTO}")
except Exception as e:
    print(f"No se pudo conectar: {e}")
    sys.exit(1)

# Crear hilo para recibir mensajes (hilo daemon)
thread_recibir = threading.Thread(target=recibir_mensajes, args=(cliente_socket,), daemon=True)
thread_recibir.start()

# Enviar mensajes en el hilo principal
enviar_mensajes(cliente_socket)