# https://ffmpeg.org/ffmpeg-codecs.html#toc-Audio-Encoders

# get codec
mediainfo test.wav

# generate silence
ffmpeg -f lavfi -i anullsrc=r=8000:cl=mono -t 60 -acodec aac silence_48.wav
ffmpeg -i silence_48.wav -b:a 128k silence.wav
rm silence_48.wav


# concatenate files
ffmpeg -i silence.wav -i test.wav  -filter_complex concat=a=1:v=0 -c:a libmp3lame -q:a 4 lc.wav
rm silence.wav
ffmpeg -i lc.wav -i silence.wav  -filter_complex concat=a=1:v=0 -c:a libmp3lame -q:a 4 lcr.wav
rm lc.wav
rm test.wav
ffmpeg -i lcr.wav -b:a 128k lcr_128.wav
rm lcr.wav
