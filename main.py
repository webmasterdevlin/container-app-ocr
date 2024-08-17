import json
import sys
import time
import logging
import threading
import uvicorn
from azure.servicebus import ServiceBusReceivedMessage
from fastapi import FastAPI

from common.message_bus import MessageBus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

receive_queue_name = "ocr_queue"
send_queue_name = "nlp_queue"

MSG_BUS = MessageBus()
MSG_BUS.connect()

app = FastAPI()


def simulate_long_processing():
    logging.info("Simulating long processing task...")
    time.sleep(9999)
    logging.info("Long processing task completed.")


def simulate_short_processing():
    logging.info("Simulating short processing task...")
    time.sleep(99)
    logging.info("Short processing task completed.")


def callback(msg: ServiceBusReceivedMessage) -> None:
    # simulate_long_processing()
    simulate_short_processing()
    body_str = b''.join(msg.body).decode('utf-8')
    input_data = json.loads(body_str)
    logging.info(f"Processing message: {input_data}")

    logging.info(f"Sending {input_data} to {send_queue_name}")
    MSG_BUS.send(queue=send_queue_name, msg=json.dumps(input_data))

def start_msg_bus():
    try:
        logging.info("Let's start consuming")
        MSG_BUS.start_consuming(queue=receive_queue_name, service_callback_handler=callback)
    except Exception as e:
        logging.error(f"Error starting the message bus: {str(e)}")
        sys.exit(1)


@app.on_event("startup")
async def startup_event():
    # Start the message bus in a separate thread
    msg_bus_thread = threading.Thread(target=start_msg_bus)
    msg_bus_thread.start()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


def start_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=80)


if __name__ == "__main__":
    # Start uvicorn in the main thread
    start_uvicorn()
