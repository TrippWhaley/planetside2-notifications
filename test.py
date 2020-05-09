from model.MetagameEvent import MetagameEvent
from model.EventServerEndpointStatus import EventServerEndpointStatus

# Turn these into actual unit tests at some point. Not now though...

dict = {'payload': {'event_name': 'MetagameEvent', 'experience_bonus': '25.000000', 'faction_nc': '66.666664', 'faction_tr': '16.470589', 'faction_vs': '16.470589', 'instance_id': '32586', 'metagame_event_id': '208', 'metagame_event_state': '135', 'metagame_event_state_name': 'started', 'metagame_event_dict': {'208': 'Terran Always Wins in Testing!'}, 'timestamp': '1588990087', 'world_id': '17'}, 'service': 'event', 'type': 'serviceMessage'}
result_payload = dict.get("payload")
alert = MetagameEvent(**result_payload)
print(alert.toString())

dict = {'detail': 'EventServerEndpoint_Emerald_17', 'online': 'false', 'service': 'event', 'type': 'serviceStateChanged'}
alert = EventServerEndpointStatus(**dict)
print(alert.isOnline(), alert.getWorld(), alert.toString())
