from flask import Flask, json, request, jsonify

PORT = 8888
API = Flask(__name__)

@API.get("")