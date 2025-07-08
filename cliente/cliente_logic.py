import sys
import socket

def recibir_mensajes(sock):
    while True:
            try:
                # recibir mensajes de hasta 1024 bytes
                mensaje = sock.recv(1024)

                # si no hay mensaje, se desconecto del servidor
                if not mensaje:
                    print("\nDesconectado del servidor")
                    sys.exit(0)

                # con decode() transformamos bytes a texto e imprimimos inmediatamente con flush
                print(f"\n{mensaje.decode('utf-8')}\n> ", end='', flush=True)
            
            # si algo falla, cerramos el sock y la conexion 
            except Exception as e:
                print(f"\nError recibiendo: {e}")
                sock.close()
                sys.exit(1)

def enviar_mensajes(sock):
    try:
        # solicitamos al usuario un nombre, encode() transforma texto a bytes y sendall manda todos los bytes
        nombre = input("Elegí tu nombre: ")
        sock.sendall(f"/nombre {nombre}".encode('utf-8'))

        while True:
            # esperando lo que escriba el usuario
            mensaje = input()

            # si el mensaje es /exit, cierra comunicacion, cierra sock y termina programa
            if mensaje.strip() == "/exit":
                print("Desconectando...")
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                sys.exit(0)

            # si no, enviamos el mensaje al servidor en formato bytes
            sock.sendall(mensaje.encode('utf-8'))

    # si algo falla, desconectamos sock y terminamos programa
    except Exception as e:
        print(f"\nError enviando: {e}")
        sock.close()
        sys.exit(1)
