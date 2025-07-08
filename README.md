# Socket Chat Grupal 

Este proyecto implementa un **chat en tiempo real** usando `sockets` y `threading`, donde múltiples clientes pueden conectarse a un servidor TCP, enviar mensajes, y recibir respuestas en tiempo real.

---
## Objetivo

Habilidades a adquirir durante el challenge:

- Manejo básico de sockets y programación de red.
- Concurrencia usando select y threading.
- Lógica de broadcast entre múltiples clientes.
- Manejo de errores y desconexiones sin que se rompa todo.

---
## Arquitectura

El proyecto se divide en los siguientes módulos:

- `/servidor/`: Servidor principal del chat, separado en dos archivos. `servidor_main.py` ejecucion del servidor y `servidor_logic` funciones auxiliares 
- `/cliente/`: Contiene el ejecutable del cliente `client_main.py` y sus funciones asociadas el envio y recepcion de mensaje `cliente_logic.py`.

---
##  Cómo usar

1. Cloná el repositorio:
   ```
    git clone https://github.com/tu-usuario/socket-chat-grupal.git
    cd socket-chat-grupal
   ```
2. Ejecutar el servidor:
   ```
    python servidor/server_main.py <IP> <PUERTO>
    //ejemplo//
    python servidor/server_main.py 127.0.0.1 3000
   ```
2. Ejecutar los clientes: En otra terminal u otra computadora conectada a la misma red
   ```
    python cliente/cliente.py <IP> <PUERTO>
    //ejemplo//
    python cliente/cliente.py 127.0.0.1 3000
   ```

---
##  Funcionalidades

- Envío de mensajes en tiempo real.
- Uso de /nombre TuNombre para identificarse.
- Comando /exit para salir del chat de forma limpia.
- Uso de select para manejar múltiples clientes sin threads en el servidor.
- Separación clara de responsabilidades: lógica y punto de entrada.
- Manejo de errores y desconexión segura.
- Ignora el reenvío del mensaje al emisor.
- Imprime los mensajes de otros usuarios en nuevas líneas sin interferir con el input.

---
## Requisitos

```
Python 3.6.X
Conexión de red entre el servidor y los clientes
```

---
## Autor

Alejandro A.

Desarrollador en constante formación.

GitHub: @alevarriola

---
## Licencia

Este proyecto está bajo la Licencia MIT.
Consultá el archivo LICENSE para más información.

---
