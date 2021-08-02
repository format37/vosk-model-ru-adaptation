#!/usr/bin/env python3

import asyncio
import websockets
import sys
import os

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        
        def get_files(path):
            for root, dirs, files in os.walk(path):
                files.sort()
                return files
        counter = 0

        for file in get_files(sys.argv[2]):
            print(' = = [',counter,'] = =',file)
            #phrases = transcribe_vosk(sys.argv[1]+'/'+file, model)
            counter += 1
            if counter > int(sys.argv[1]):
                break
            wf = open(sys.argv[2]+file, "rb")

            while True:
                data = wf.read(8000)

                if len(data) == 0:
                    break

                await websocket.send(data)
                print (await websocket.recv())
        await websocket.send('{"eof" : 1}')
        print (await websocket.recv())

asyncio.get_event_loop().run_until_complete(
    hello('ws://localhost:2700'))
