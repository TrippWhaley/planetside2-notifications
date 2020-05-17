from dataclasses import dataclass
from datetime import datetime

@dataclass
class MetagameEvent:
  event_name: str
  experience_bonus: str
  instance_id: str
  metagame_event_id: str
  metagame_event_state: str
  metagame_event_state_name: str
  metagame_event_dict: dict
  faction_tr: str
  faction_nc: str
  faction_vs: str
  world_id: str
  timestamp: str
  def toString(self):
      	return  """
	ALERT:
	Terran Republic: {}
	New Conglomerate: {}
	Vanu Scum: {}
    {}
	{} at {}
      			""".format(self.faction_tr, self.faction_nc, self.faction_vs, self.metagame_event_dict[self.metagame_event_id], self.metagame_event_state_name, datetime.fromtimestamp(int(self.timestamp)).strftime("%H:%M:%S"))
