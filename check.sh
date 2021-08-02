#!/bin/bash
sudo docker cp $(cat docker_id.txt):/opt/vosk-model-ru/model /media/alex/nvme-a/
python3 check_model.py /media/alex/nvme-a/word_5 /media/alex/nvme-a/model $1
