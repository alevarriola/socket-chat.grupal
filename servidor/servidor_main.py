import socket
import select
import sys
from servidor_logic import manejar_cliente


# Crear socket TCP (stream) para IPv4
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permitir reusar la dirección si reiniciás rápido
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Validar argumentos sys.argv es una lista con los argumentos que pasaste al ejecutar el programa
if len(sys.argv) != 3:
    print("Uso: python servidor.py <IP> <PUERTO>")
    sys.exit(1)

IP = str(sys.argv[1])     # IP desde línea de comandos
PUERTO = int(sys.argv[2]) # Puerto desde línea de comandos

# Enlazar el socket a la IP y el puerto y Empezar a escuchar a max 10
servidor.bind((IP, PUERTO))
servidor.listen(10)

print(f"Servidor escuchando en {IP}:{PUERTO}")

# Lista de sockets activos y dic de socket => nombre
sockets_activos = [servidor]
clientes = {}
try: 
    while True:
        # Esperar actividad en cualquier socket activo (Devuelve los sockets que tienen datos para leer)
        sockets_lectura, _, _ = select.select(sockets_activos, [], [], 1)

        for socket_actual in sockets_lectura:

            # Si el socket actual es el servidor significa alguien nuevo quiere conectarse
            if socket_actual == servidor:
                cliente, direccion = servidor.accept()
                sockets_activos.append(cliente)
                clientes[cliente] = None
                print(f"[+] Nuevo cliente conectado desde {direccion}")

            # Si es un cliente que ya estaba conectado, leer mensaje
            else:
                manejar_cliente(socket_actual, servidor, sockets_activos, clientes)

# interrupcion de servidor        
except KeyboardInterrupt:
    print("\n[!] Servidor interrumpido con Ctrl+C. Cerrando conexiones...")

# limpieza de todo cuando se cierra el servidor
finally:
    for sock in sockets_activos:
        try:
            sock.close()
        except:
            pass
    servidor.close()
    sys.exit(0)