import os
import sys
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

def transcribe_vosk(file_name, model_path):

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
    model = Model(model_path)
    rec = KaldiRecognizer(model, fr)

    # recognizing
    while True:

        conf_score = []

        data = wf.readframes(4000)
        if len(data) == 0:
            break
        else:
            print('data', len(data))

        if rec.AcceptWaveform(data):
            accept = json.loads(rec.Result())
            print('d', accept)
            if accept['text'] !='':
                print(accept['text'])
                phrases_list.append(accept['text'])
    return phrases_list

def get_files(path):
    for root, dirs, files in os.walk(path):
        files.sort()
        return files

print('start')
phrases = transcribe_vosk(sys.argv[1], sys.argv[2])
print(phrases)
print('end')
