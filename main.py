import os
from waitress import serve
from flask import Flask, request, jsonify, send_from_directory
import requests
import platform

app = Flask(__name__)

my_secret = os.environ['ERD_API_KEY']


def getPlatform():
  return platform.system()


def get_exchange_rate(from_currency, to_currency, amount, date=None):
  url = f"https://api.apilayer.com/exchangerates_data/convert?from={from_currency}&to={to_currency}&amount={amount}"

  headers = {"apikey": my_secret}

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    result = response.json()
    return result["result"]
  else:
    raise Exception(f"Error: {response.status_code}, {response.text}")


# @app.route('/settings', methods=['GET'])
# def convert_currency():
#   from_currency = request.args.get('requirement')  # user's requirement
#   to_currency = request.args.get('to')
#   amount = request.args.get('amount')
#   date = request.args.get('date', None)

#   try:
#     converted_amount = get_exchange_rate(from_currency, to_currency, amount,
#                                          date)
#     platform = getPlatform()
#     return jsonify({
#       "from": from_currency,
#       "to": to_currency,
#       "amount": amount,
#       "converted_amount": converted_amount,
#       "message": "test"
#     })
#   except Exception as e:
#     return jsonify({"error": str(e)}), 400


@app.route('/convert', methods=['GET'])
def change_config():
  linkUrl = "https://fhlkm.github.io/configuration/?command="
  command = request.args.get('command')
  print(command)
  description = "I will do your command , please open this link:"
  if (command == "Mute Device"):
    linkUrl = linkUrl + str(1111)
  elif (command == "unMute Device"):
    linkUrl = linkUrl + str(2222)
  elif (command == "Block Camera"):
    linkUrl = linkUrl + str(3333)
  elif (command == "Unblock Camera"):
    linkUrl = linkUrl + str(4444)
  elif (command == "Change brightness"):
    linkUrl = linkUrl + str(5555)
  else:
    linkUrl = ""
    description = "This url will change user's configuration"
  try:

    return jsonify({
      "url": linkUrl,
      "command": command,
      "description": description
    })
  except Exception as e:
    return jsonify({"error": str(e)}), 400
@app.route('/setaction', methods=['GET'])
def set_action():
  linkUrl = "https://fhlkm.github.io/configuration/?"
  condition = request.args.get('condition')
  action = request.args.get('action')
  description = "I will do your action , please open this link:"
  linkUrl = linkUrl +condition+"="+action
  print(linkUrl)
  try:

    return jsonify({
      "url": linkUrl,
      "condition": condition,
      "action": action,
      "description": description
    })
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)
