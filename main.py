import asyncio
import json
import requests
from time import sleep
from datetime import datetime
from websocket import create_connection
from model.MetagameEvent import MetagameEvent

# TODO: create various subsciptions for events like Sean dying in game and shaming him when he spends certs
world_name = "Emerald"
event_name = "MetagameEvent"
payload_tpl = """
{{
	"service":"event",
	"action":"subscribe",
	"worlds":["{}"],
	"eventNames":["{}"]
}}
"""

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

payload = payload_tpl.format(world_dict.get("Emerald"), event_name)

# TODO: dump these in a function to recreate the connection when it eventually craps out
ws = create_connection(
    "wss://push.planetside2.com/streaming?environment=ps2&service-id=s:example"
)
ws.send(payload_tpl)


# Run until it can't run no more
def main():
	try:
		while (True):
			result = ws.recv()
			dict = json.loads(result)
			# 99% of events are heartbeats regardless of the payload, and that ain't certs
			if (dict.get("payload") is not None):
				result_payload = dict.get("payload")
				try:
					alert = MetagameEvent(**result_payload)
					# TODO: hook into Justin's discord bot
					print(alert.toString())
				except Exception as e:
					print(e)
			sleep(5)
	except Exception as e:
		# change this to reconnect with exponential backoff retry logic later
		print(e)
		ws.close()

if __name__ == '__main__':
	main()
