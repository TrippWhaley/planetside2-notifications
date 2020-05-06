import json
import time
from websocket import create_connection

# TODO: create various subsciptions for events like Sean dying in game and shaming him when he spends certs
payload = """
{
	"service":"event",
	"action":"subscribe",
	"worlds":["all"],
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
        js = json.loads(result)
        try:
            # 99% of events are heartbeats regardless of the payload, and that ain't certs
            if (js["type"] != "heartbeat"):
                # TODO: hook into Justin's discord bot
                print(js)
        except:
            pass
    except:
        # whenever the connection craps out I just wanna know how long the process lasted and break outta the loop so it doesn't run forever, for now at least
        print(time.localtime())
        break
    time.sleep(10)
