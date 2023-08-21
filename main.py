import websocket._app as websocket_app
import json
import uuid
import os
import dotenv

dotenv.load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

def on_message(ws, message):
    data = json.loads(message)
    if data['type'] == 'messages':
        print(f"Received {len(data['messages'])} messages.")
        for msg in data['messages']:
            print(msg)
    else:
        print(f"Received: {message}")

def on_open(ws):
    print("WebSocket opened.")
    # Send a message to request chat messages
    request = {
        "action": "requestMessages",
        "chatRoomId": "0x85f8c70a0ab0c948a3ed0236e2cc245719ae084c",
        "pageStart": None
    }
    ws.send(json.dumps(request))


def send_message(ws, text):
    message = {
        "action": "sendMessage",
        "text": text,
        "imagePaths": None,
        "chatRoomId": "0x85f8c70a0ab0c948a3ed0236e2cc245719ae084c",
        "clientMessageId": str(uuid.uuid4())  # Generate a unique ID
    }
    ws.send(json.dumps(message))
    print(f"Sent message: {text}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

if __name__ == "__main__":
    websocket_url = F"wss://prod-api.kosetto.com?authorization={AUTH_TOKEN}"
    ws = websocket_app.WebSocketApp(websocket_url,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()
