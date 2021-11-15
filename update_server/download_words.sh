#if [ -f "../model_files/words.txt" ]; then rm -r ../model_files/words.txt; fi 
/usr/bin/docker cp vosk-model-ru-adaptation_server_z_1:/opt/vosk-model-ru/model/graph/words.txt ../model_files/
