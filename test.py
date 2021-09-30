import os
import asyncio
import websockets
import json
import datetime

time_start = datetime.datetime.now()

async def transcribe_vosk(file_path):
    async with websockets.connect('ws://'+os.environ.get('VOSK_SERVER_IP', '')+':2700') as websocket:
        
        phrases = []
        with open(file_path, "rb") as audio_file:
            while True:
                data = audio_file.read(16000) # 8000
                #if len(data) == 0:
                if not data:
                    break
                await websocket.send(data)
                accept = json.loads(await websocket.recv())
                if len(accept)>1 and accept['text'] != '':
                    accept_text = str(accept['text'])
                    phrases.append(accept_text)

            await websocket.send('{"eof" : 1}')
            accept = json.loads(await websocket.recv())
            if len(accept)>1 and accept['text'] != '':
                accept_text = str(accept['text'])
                phrases.append(accept_text)

    return phrases

def get_files(path):
    for root, dirs, files in os.walk(path):
        files.sort()
        return files

print('start')
path = 'files/'
for file in get_files(path):
    print(datetime.datetime.now(), file)
    phrases = asyncio.get_event_loop().run_until_complete(transcribe_vosk(path + file))
    print(phrases)

time_end = datetime.datetime.now()
print('spent', (time_end - time_start).seconds, 'seconds')
