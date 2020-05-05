import json
import requests

character_name = "Diabeast"
base_url = "http://census.daybreakgames.com/get/ps2:v2/character/?name.first_lower={}".format(character_name.lower())

character_response = requests.get(base_url)
character_id = json.loads(character_response.text)["character_list"][0]["character_id"]

friends = requests.get("http://census.daybreakgames.com/get/ps2:v2/characters_friend/?character_id={}".format(character_id))
list = json.loads(friends.text)["characters_friend_list"][0]["friend_list"]

for c in list:
    friend = json.loads(requests.get("http://census.daybreakgames.com/get/ps2:v2/character/?character_id={}".format(c["character_id"])).text)
    print(friend["character_list"][0]["name"]["first"], friend["character_list"][0]["certs"]["available_points"])

print(json.loads(requests.get("http://census.daybreakgames.com/get/ps2:v2/map/?world_id=1&zone_ids=2").text))
