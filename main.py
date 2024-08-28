import json
import logging

from azure.servicebus import ServiceBusReceivedMessage

from common.message_bus import MessageBus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

receive_queue_name = "ocr_queue"
send_queue_name = "nlp_queue"

MSG_BUS = MessageBus()
MSG_BUS.connect()

def callback(msg: ServiceBusReceivedMessage) -> None:
    body_str = b''.join(msg.body).decode('utf-8')
    input_data = json.loads(body_str)
    logging.info(f"Processing message: {input_data}")

    logging.info(f"Sending {input_data} to {send_queue_name}")
    MSG_BUS.send(queue=send_queue_name, msg=json.dumps(input_data))

if __name__ == "__main__":
    logging.info("OCR in VM is starting..")
    MSG_BUS.start_consuming(queue=receive_queue_name, service_callback_handler=callback)

