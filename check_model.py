import os
import sys
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

def transcribe_vosk(file_name, model):

    # https://alphacephei.com/vosk/
    phrases_list = []

    # read file
    wf = wave.open(file_name, "rb")
    fr = wf.getframerate()
    nframes = wf.getnframes()

    print('framerate', fr)
    print('number of audio frames', nframes)
    print('params', wf.getparams())
    # exit()
    # read model
        
    rec = KaldiRecognizer(model, fr)

    # recognizing
    while True:
        
        conf_score = []

        data = wf.readframes(4000)
        if len(data) == 0:
            break
        #else:
        #print('data', len(data))

        if rec.AcceptWaveform(data):                
            try:
                #print('requiring rec result')
                rec_result = rec.Result()
                #print('successfully required rec result')
                accept = json.loads(rec_result)
                #print('d', accept)
                if accept['text'] !='':
                    #print(accept['text'])
                    phrases_list.append(accept['text'])
            except Exception as e:
                print('error:', str(e))
    return phrases_list

def get_files(path):
    for root, dirs, files in os.walk(path):
        files.sort()
        return files

print('model init..')
model = Model(sys.argv[2])
print('start')
#phrases = transcribe_vosk(sys.argv[1], sys.argv[2])
counter = 0
for file in get_files(sys.argv[1]):
    print(' = = [',counter,'] = =',file)
    phrases = transcribe_vosk(sys.argv[1]+'/'+file, model)
    counter += 1
    if counter > int(sys.argv[3]):
        break
    print(phrases)
print('end')
