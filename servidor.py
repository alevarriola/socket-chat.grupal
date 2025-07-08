import socket
import select
import sys

def broadcast(mensaje, servidor, sockets_activos, clientes, emisor=None):

    # recorremos todos nuestros sock, mientras no sea el mismo y el servidor
    for sock in sockets_activos[:]:  # : iterar sobre copia
        if sock != servidor and sock != emisor:
            try:
                # enviamos mensaje codificado
                sock.sendall(mensaje.encode('utf-8'))

            # si falla el envio por desconexion
            except Exception:

                # eliminamos al cliente del sock
                nombre = clientes.get(sock, "Anonimo")
                print(f"[!] Error enviando a {nombre}, cerrando socket")
                if sock in sockets_activos:
                    sockets_activos.remove(sock)
                clientes.pop(sock, None)
                try:
                    sock.close()
                except:
                    pass

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
                try:
                    # Leer hasta 1024 bytes de datos del cliente
                    mensaje_bytes = socket_actual.recv(1024)

                    # Si no hay datos, el cliente se desconectó
                    if not mensaje_bytes:

                        # informamos deconexion
                        nombre = clientes.get(socket_actual, "Anonimo")
                        print(f"[-] {nombre} se desconectó")
                        broadcast(f"{nombre} salió del chat.", servidor, sockets_activos, clientes)

                        # se elimina sock y dato del cliente
                        if socket_actual in sockets_activos:
                            sockets_activos.remove(socket_actual)
                        clientes.pop(socket_actual, None)
                        try:
                            socket_actual.close()
                        except:
                            pass
                        continue
                    
                    # si si mando algo, decodificamos mensaje del cliente
                    mensaje = mensaje_bytes.decode('utf-8').strip()

                    # asignacion de nombre
                    if mensaje.startswith("/nombre "):
                        nombre = mensaje.split(" ", 1)[1].strip()
                        clientes[socket_actual] = nombre
                        print(f"[+] Cliente asignó nombre: {nombre}")
                        broadcast(f"{nombre} se unió al chat.", servidor, sockets_activos, clientes)
                        continue
                    
                    # si no asigno, reiteramos hasta que lo asigne
                    if clientes.get(socket_actual) is None:
                        socket_actual.sendall("Primero debes enviar tu nombre con /nombre TuNombre\n".encode('utf-8'))
                        continue

                    # si tiene nombre, y no entro en ningun otro if, enviar mensaje a todos
                    nombre = clientes.get(socket_actual, "Anonimo")
                    broadcast(f"{nombre}: {mensaje}", servidor, sockets_activos, clientes, socket_actual)

                # en caso de error o interrupcion, remover al cliente
                except Exception as e:

                    # informamos a todos 
                    print(f"[!] Error con un cliente: {e}")
                    nombre = clientes.get(socket_actual, "Anonimo")
                    broadcast(f"{nombre} salió del chat por error.", servidor, sockets_activos, clientes)

                    # eliminamos datos y sock del cliente
                    if socket_actual in sockets_activos:
                        sockets_activos.remove(socket_actual)
                    clientes.pop(socket_actual, None)
                    try:
                        socket_actual.close()
                    except:
                        pass

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