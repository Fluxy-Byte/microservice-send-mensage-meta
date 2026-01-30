import pika

connection = None
channel = None


def conectar():
    global connection, channel

    url = "amqp://fluxy:oetF9RhdlKVPQEt3L3aUjRFOBmet9COfmgEZj@147.79.110.10:5672"

    params = pika.URLParameters(url)

    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    print("Rabbit conectado 🚀")


def fechar():
    global connection

    if connection:
        connection.close()
        print("Rabbit fechado ❌")
