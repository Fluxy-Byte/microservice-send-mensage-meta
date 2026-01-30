import pika
import json
from src.infra.meta.SendMensageToMeta import send_mensagem

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(queue='task.fluxy.receptive.create', durable=True)

mock = {
    "tipo_mensagem": "text",
    "numero_usuario": "5534997801829",
    "id_conversa": "wa.232132",
    "payload": "Ola como esta?"
}

# Se for do tipo audio vai vir o id do audo no payload


def callback(ch, method, properties, body):
    body_mensagem = json.loads(body)

    print("Recebi:", body_mensagem)
    payload = {}
    if body_mensagem.tipo_mensagem == "text":
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": body_mensagem.numero_usuario,
            "context": {
                "message_id": body_mensagem.id_conversa
            },
            "type": "text",
            "text": {
                "preview_url": False,
                "body": body_mensagem.payload
            }
        }
        print(payload)
    elif body_mensagem.tipo_mensagem == "audio":
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": body_mensagem.numero_usuario,
            "context": {
                "message_id": body_mensagem.id_conversa
            },
            "type": "audio",
            "audio": {
                "id": body_mensagem.payload
            }
        }
        print(payload)
    
    # Simula processamento
    print("Processando...")
    send_mensagem(payload)
    # Confirma que processou
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue='task.fluxy.receptive.create',
    on_message_callback=callback
)

print("Aguardando mensagens...")

channel.start_consuming()
