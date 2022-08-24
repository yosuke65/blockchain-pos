from flask_classful import FlaskView, route
from flask import Flask


class NodeAPI(FlaskView):
  
  def __init__(self):
    self.app = Flask(__name__)
    
  def start(self):
    NodeAPI.register(self.app, route_base='/')
    self.app.run(host='localhost', port=5500)
    
  @route('/info', methods=['GET'])
  def info(self):
    return 'This is a communication interface to the nodes in the blockchain network.', 200