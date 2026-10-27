from flask import Flask, request, jsonify

# Define the Flask app
app = Flask(__name__)

subscribers = {}
subject = ""

def home():
  return "Hello from Flask!"

# curl -X POST -H "Content-Type: application/json" -d '{"name":"Grace","URI":"http://grace.example.com"}' http://localhost:5000/add-subscriber
# curl -X POST -H "Content-Type: application/json" -d '{"name":"Ada","URI":"http://ada.site.com"}' http://localhost:5000/add-subscriber
# curl -X POST -H "Content-Type: application/json" -d '{"name":"Alan","URI":"http://alan.site.com"}' http://localhost:5000/add-subscriber
@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():
  data = request.json
  name = data.get('name')
  URI = data.get('URI')
  subscribers[name] = URI
  print(f"You entered: Name={name}, Address={URI}")
  return jsonify({'message': f'You sent name: {name} and address: {URI}'})

# curl http://localhost:5000/list-subscribers
@app.route('/list-subscribers', methods=['GET'])
def listSubscribers():
  return jsonify(subscribers)

# curl -X DELETE -H "Content-Type: application/json" -d '{ "name":"Grace" }' http://localhost:5000/delete-subscriber
# curl -X DELETE -H "Content-Type: application/json" -d '{ "name":"Bob" }' http://localhost:5000/delete-subscriber
@app.route('/delete-subscriber', methods=['DELETE'])
def deleteSubscriber():
  data = request.json
  name = data.get('name')
  if name in subscribers:
    del subscribers[name]
    print(f"You entered: Name={name}")
    return jsonify({'message': f'You deleted name: {name}'})
  else:
    return jsonify({'message': f'Could not find name: {name}'})

# curl -X POST -H "Content-Type: application/json" -d '{"subject-update":"Hello world!"}' http://localhost:5000/update-and-notify
@app.route('/update-and-notify', methods=['POST'])
def updateAndNotifyAllSubscribers():
  data = request.json
  subject = data.get('subject-update')
  print(f"You updated the subject to: {subject}")
  for key in subscribers.keys():
    print(f"Notifying {key} at {subscribers[key]} of the new subject: {subject}")
  return jsonify({'message': f'You updated subject to: {subject} '})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)