from flask import request, jsonify
from Application.Service.user_service import UserService

class UserController: 
  def __init__(self, user_service):
      self.user_service = user_service
      

  def register(self):
    data = request.get_json()
    result = self.user_service.register_user(data) 
    return jsonify(result), 201

  
  def activate(self):
    data = request.get_json()
    result = self.user_service.activate_user(data)
    return jsonify(result), 201

 
  def login(self):
    data = request.get_json()
    result = self.user_service.login_user(data)
    return jsonify(result), 201