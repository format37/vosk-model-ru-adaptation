if [ -f "../model_files/words.txt" ]; then sudo rm -r ../model_files/words.txt; fi 
sudo docker cp vosk-model-ru-adaptation_server_x_1:/opt/vosk-model-ru/model/graph/words.txt ../model_files/
