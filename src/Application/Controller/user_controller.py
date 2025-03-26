from flask import request, jsonify
from Application.Service.user_service import UserService

class UserController: 
  def __init__(self):
      self.user_service = UserService()
      
  @staticmethod
  def register():
    data = request.get_json()
    result = UserService.register_user(data) 
    return jsonify(result), 201

  @staticmethod
  def activate():
    data = request.get_json()
    result = UserService.activate_user(data)
    return jsonify(result), 201

  @staticmethod
  def login():
    data = request.get_json()
    result = UserService.login_user(data)
    return jsonify(result), 201