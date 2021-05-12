import asyncio
import websockets
import json
import os
import requests
from dotenv import load_dotenv

import model.alert as alerts
from model.census import World
from model.alert.base import Alert

# load env
load_dotenv()
discord_webhook = os.getenv("DISCORD_WEBHOOK")
world_name = os.getenv("WORLD_NAME")
event_name = os.getenv("EVENT_NAME")
ps2_env = os.getenv("PS2_ENV")
service_id = os.getenv("SERVICE_ID")

# Init static data models
world_dict = World()
alert_models = dict([(name, cls) for name, cls in alerts.__dict__.items() if isinstance(cls, type)])

# Format connection specific stuffs
payload_tpl = """
{{
	"service":"event",
	"action":"subscribe",
	"worlds":["{}"],
	"eventNames":["{}"]
}}
"""
ws_url_tpl = "wss://push.planetside2.com/streaming?environment={}&service-id=s:{}"
payload = payload_tpl.format(world_dict.get(world_name), event_name)
ws_url = ws_url_tpl.format(ps2_env, service_id)

# Send discord notification with webhook
def send_discord_alert(alert: Alert):
	print(alert.to_string())
	return requests.post(url = discord_webhook, data = {'content': alert})

# Create discord notification if message type is valid
def process_message(message):
	try:
		data = json.loads(message)
		for alert_model in alert_models:
			alert: Alert = getattr(alerts, alert_model).from_dict(data)
			if alert is not None:
				send_discord_alert(alert)
	except Exception as e:
		print(e)

async def consume(ws_url, payload):
	async with websockets.connect(ws_url) as ws:
		await ws.send(payload)
		async for message in ws:
			process_message(message)
			# sleep(1)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(consume(ws_url, payload))
	loop.run_forever()
