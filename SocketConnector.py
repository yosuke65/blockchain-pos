
class SocketConnector():
  
  def __init__(self, ip, port):
     self.ip = ip
     self.port = port
     
  def equals(self, socketConnector):
    if self.ip == socketConnector.ip and self.port == socketConnector.port:
      return True
    return False