import socket
import select
import sys


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

# Lista de sockets activos (servidor + clientes)
sockets_activos = [servidor]

while True:
    # Esperar actividad en cualquier socket activo (Devuelve los sockets que tienen datos para leer)
    sockets_lectura, _, _ = select.select(sockets_activos, [], [])

    for socket_actual in sockets_lectura:

        # Si el socket actual es el servidor → alguien nuevo quiere conectarse
        if socket_actual == servidor:
            cliente, direccion = servidor.accept()
            sockets_activos.append(cliente)
            print(f"[+] Nuevo cliente conectado desde {direccion}")

        # Si es un cliente que ya estaba conectado → leer mensaje
        else:
            try:
                # Leer hasta 1024 bytes de datos del cliente
                mensaje = socket_actual.recv(1024)

                # Si no hay datos, el cliente se desconectó
                if not mensaje:
                    print("[-] Cliente desconectado")
                    sockets_activos.remove(socket_actual)
                    socket_actual.close()
                    continue

                # recorrer todos los otros que esten en activos
                for otro_socket in sockets_activos:
                    if otro_socket != servidor and otro_socket != socket_actual:
                        # Reenviar el mensaje a todos menos el que lo mandó
                        otro_socket.sendall(mensaje)

            except Exception as e:
                print(f"[!] Error con un cliente: {e}")
                sockets_activos.remove(socket_actual)
                socket_actual.close()