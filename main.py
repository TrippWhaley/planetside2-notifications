import asyncio
from datetime import datetime
from dotenv import load_dotenv
import json
import os
import websockets

import model.alert as alerts
from model.census import World
from model.alert.base import Alert

# Load env
load_dotenv()
discord_webhook = os.getenv("DISCORD_WEBHOOK")
world_name = os.getenv("WORLD_NAME")
event_name = os.getenv("EVENT_NAME")
ps2_env = os.getenv("PS2_ENV")
service_id = os.getenv("SERVICE_ID")

# Init static data models
world_dict = World()
alert_models = dict(
    [(name, cls) for name, cls in alerts.__dict__.items() if isinstance(cls, type)]
)

# Format connection specific stuffs
payload = f"""
{{
	"service":"event",
	"action":"subscribe",
	"worlds":["{world_dict.get(world_name)}"],
	"eventNames":["{event_name}"]
}}
"""
ws_url = f"wss://push.planetside2.com/streaming?environment={ps2_env}&service-id=s:{service_id}"

# Create discord notification if message type is valid
def process_message(message):
    try:
        data = json.loads(message)
        for alert_model in alert_models:
            alert: Alert = getattr(alerts, alert_model).from_dict(data)
            if alert is not None:
                alert.send_discord(discord_webhook)
    except Exception as e:
        print(e)


async def consume(ws_url, payload):
    async with websockets.connect(ws_url) as ws:
        await ws.send(payload)
        async for message in ws:
            process_message(message)


if __name__ == "__main__":
    print(f"Resumed execution at UTC {datetime.utcnow().strftime('%H:%M:%S')}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(ws_url, payload))
    loop.run_forever()
