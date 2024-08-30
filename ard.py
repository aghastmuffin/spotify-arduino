import requests
import serial
import webbrowser
import websockets
import asyncio
from time import sleep

# Serial Port Configuration
ser = serial.Serial('COM3', 9600)
ser.write(b'Connected to Python/awaiting verification')
# Spotify API Credentials
CLIENT_ID = 'deedcb69176e4f00be03b6b1ab26b234'
CLIENT_SECRET = 'bab57ca07cd241e4a395ac6e6965125d'
REDIRECT_URI = 'https://aghastmuffin.github.io/webhome/spotify/'
SCOPE = 'user-read-currently-playing'

# Global Variables
authorization_code = ""
access_token = ""


def get_auth_code():
    auth_url = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}'
    print("Opening authentication window...")
    webbrowser.open(auth_url)

async def exchange_code_for_token():
    global authorization_code, access_token
    try:
        authorization_code = input("?auth?:" )
    except Exception as e:
        print(f"WebSocket server error: {e}")
    
    if authorization_code:
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        response = requests.post(token_url, data=token_data)
        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info['access_token']
        else:
            print("Error obtaining access token:", response.text)

def make_api_request():
    global access_token
    while True:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "item" in data:
                try:
                    track_info = f'{data["item"]["name"]}/{data["item"]["album"]["artists"][0]["name"]}'
                    ser.write(track_info.encode('utf-8'))
                except:
                    ser.write(b'No song\\artist/podcast?')
            else:
                ser.write(b'No song playing/No artist playing')
        else:
            print("ERROR! Failed to fetch data from Spotify.")
            print(response.text)
            print("Status Code:", response.status_code)
        
        sleep(4)

async def main():
    get_auth_code()
    await exchange_code_for_token()
    if access_token:
        make_api_request()

asyncio.run(main())
