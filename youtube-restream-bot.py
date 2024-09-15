import requests
import time
import obswebsocket, obswebsocket.requests

# Configuration
API_KEY = 'YOUR_YOUTUBE_API_KEY'
CHANNEL_ID = 'YOUR_YOUTUBE_CHANNEL_ID'
OBS_WEBSOCKET_HOST = 'localhost'
OBS_WEBSOCKET_PORT = 4444
OBS_WEBSOCKET_PASSWORD = 'YOUR_OBS_WEBSOCKET_PASSWORD'
CHECK_INTERVAL = 60  # Check every 60 seconds

def is_channel_live(api_key, channel_id):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&eventType=live&key={api_key}'
    response = requests.get(url)
    data = response.json()
    return len(data['items']) > 0

def start_obs_stream():
    client = obswebsocket.obsws(OBS_WEBSOCKET_HOST, OBS_WEBSOCKET_PORT, OBS_WEBSOCKET_PASSWORD)
    client.connect()
    client.call(obswebsocket.requests.StartStreaming())
    client.disconnect()

while True:
    if is_channel_live(API_KEY, CHANNEL_ID):
        print("Channel is live! Starting OBS stream...")
        start_obs_stream()
        break
    else:
        print("Channel is not live. Checking again in 60 seconds.")
    time.sleep(CHECK_INTERVAL)
