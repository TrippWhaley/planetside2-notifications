from dataclasses import dataclass
from datetime import datetime

@dataclass
class EventServerEndpointStatus:
  detail: str
  online: str
  service: str
  type: str
  def isOnline(self):
      return self.online == "true"
  def getWorld(self):
      s = self.detail
      return s[s.find("_")+1:s.rfind("_")]
  def toString(self):
      return "EventServerEndpoint for {} is {}online".format(self.getWorld(), "" if self.isOnline() else "not ")
