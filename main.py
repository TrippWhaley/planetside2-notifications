import asyncio
import websockets
import json
import requests
import os
from time import sleep
from datetime import datetime
from model.MetagameEvent import MetagameEvent
from model.EventServerEndpointStatus import EventServerEndpointStatus
from dotenv import load_dotenv

# load env
load_dotenv()
discord_webhook = os.getenv("DISCORD_WEBHOOK")
world_name = os.getenv("WORLD_NAME")
event_name = os.getenv("EVENT_NAME")
ps2_env = os.getenv("PS2_ENV")
service_id = os.getenv("SERVICE_ID")

# Init static data models
zone_list = json.loads(requests.get("http://census.daybreakgames.com/json/get/ps2:v2/zone/?c:limit=100").text).get("zone_list")
zone_dict = {}
for zone in zone_list:
	zone_dict[zone.get("zone_id")] = zone.get("code")

world_list = json.loads(requests.get("http://census.daybreakgames.com/json/get/ps2:v2/world/?c:limit=100").text).get("world_list")
world_dict = {}
for world in world_list:
	world_dict[world.get("name").get("en")] = world.get("world_id")

metagame_event_list = json.loads(requests.get("http://census.daybreakgames.com/json/get/ps2:v2/metagame_event/?c:limit=1000").text).get("metagame_event_list")
metagame_event_dict = {}
for metagame_event in metagame_event_list:
	metagame_event_dict[metagame_event.get("metagame_event_id")] = metagame_event.get("name").get("en")

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
def send_discord_alert(alert):
	return requests.post(url = discord_webhook, data = {'content': alert})

# Create discord notification if message type is valid
def process_message(message):
	dict = json.loads(message)
	if (dict.get("payload") is not None):
		model = MetagameEvent
		dict = dict.get("payload")
		dict["metagame_event_dict"] = metagame_event_dict
	elif (dict.get("detail") is not None):
		model = EventServerEndpointStatus
	else:
		return
	try:
		alert = model(**dict)
		# TODO: use discord bot
		send_discord_alert(alert.toString())
	except Exception as e:
		print(e)

async def consume(ws_url, payload):
	async with websockets.connect(ws_url) as ws:
		await ws.send(payload)
		async for message in ws:
			process_message(message)
			sleep(1)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(consume(ws_url, payload))
	loop.run_forever()
