import socket
import select

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

def manejar_cliente(socket_actual, servidor, sockets_activos, clientes):
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
            socket_actual.close()
            return
        
        # si si mando algo, decodificamos mensaje del cliente
        mensaje = mensaje_bytes.decode('utf-8').strip()

        # asignacion de nombre
        if mensaje.startswith("/nombre "):
            nombre = mensaje.split(" ", 1)[1].strip()
            clientes[socket_actual] = nombre
            print(f"[+] Cliente asignó nombre: {nombre}")
            broadcast(f"{nombre} se unió al chat.", servidor, sockets_activos, clientes)
            return
        
        # si no asigno, reiteramos hasta que lo asigne
        if clientes.get(socket_actual) is None:
            socket_actual.sendall("Primero debes enviar tu nombre con /nombre TuNombre\n".encode('utf-8'))
            return

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