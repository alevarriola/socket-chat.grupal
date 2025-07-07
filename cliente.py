import socket
import sys
import threading

def recibir_mensajes(sock):
    while True:
            try:
                mensaje = sock.recv(1024)
                if not mensaje:
                    print("\nDesconectado del servidor")
                    sys.exit(0)
                print(f"\n{mensaje.decode('utf-8')}\n> ", end='', flush=True)
            except Exception as e:
                print(f"\nError recibiendo: {e}")
                sock.close()
                sys.exit(1)

def enviar_mensajes(sock):
    try:
        nombre = input("Elegí tu nombre: ")
        sock.sendall(f"/nombre {nombre}".encode('utf-8'))

        while True:
            mensaje = input()
            if mensaje.strip() == "/exit":
                print("Desconectando...")
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                sys.exit(0)
            sock.sendall(mensaje.encode('utf-8'))
    except Exception as e:
        print(f"\nError enviando: {e}")
        sock.close()
        sys.exit(1)


if len(sys.argv) != 3:
    print("Uso: python cliente.py <IP> <PUERTO>")
    sys.exit(1)

IP = sys.argv[1]
PUERTO = int(sys.argv[2])

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    cliente_socket.connect((IP, PUERTO))
    print(f"Conectado al servidor {IP}:{PUERTO}")
except Exception as e:
    print(f"No se pudo conectar: {e}")
    sys.exit(1)

# Crear hilo para recibir mensajes
thread_recibir = threading.Thread(target=recibir_mensajes, args=(cliente_socket,), daemon=True)
thread_recibir.start()

# Enviar mensajes en el hilo principal
enviar_mensajes(cliente_socket)