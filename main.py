import json
from time import sleep
from datetime import datetime
from websocket import create_connection

# Testing the webhook with this commit
# TODO: create various subsciptions for events like Sean dying in game and shaming him when he spends certs
payload = """
{
	"service":"event",
	"action":"subscribe",
	"worlds":["17"],
	"eventNames":["MetagameEvent"]
}
"""

# TODO: dump these in a function to recreate the connection when it eventually craps out
ws = create_connection(
    "wss://push.planetside2.com/streaming?environment=ps2&service-id=s:example"
)
ws.send(payload)

# Run until it can't run no more
while (True):
    try:
        result = ws.recv()
        dict = json.loads(result)
    except:
        # change this to reconnect with exponential backoff retry logic later
        ws.close()
        break
    # 99% of events are heartbeats regardless of the payload, and that ain't certs
    if (dict.get("payload") is not None):
        ws_payload = dict.get("payload")
        if (ws_payload.get("event_name") is not None
                and payload.get("metagame_event_id") == 210):
            # TODO: hook into Justin's discord bot
            tr = faction.get("faction_tr")
            nc = faction.get("faction_nc")
            vs = faction.get("faction_vs")
            alert = """
						ALERT STATUS:
						Terran Republic: {}
						New Conglomerate: {}
						Vanu Scum: {}
						{}
					"""
            print(alert.format(tr, nc, vs, datetime.now().time()))
    sleep(10)
