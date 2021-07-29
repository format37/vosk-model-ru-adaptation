#!/bin/bash
sudo rm -r /media/alex/nvme-a/model/
sudo docker stop $(cat docker_id.txt)
sudo docker rm $(cat docker_id.txt)
python3 word_collector.py
sudo docker run -d -p 2700:2700 alphacep/kaldi-vosk-model-ru:latest | tee docker_id.txt
#export VOSKID=$(cat docker_id.txt)
#echo $VOSKID
sudo docker cp ./corpus.txt $(cat docker_id.txt):/opt/vosk-model-ru/model/new/data/corpus
echo 'Update started. Follow the CPU utilization to catch the process complition..'
