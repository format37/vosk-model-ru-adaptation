#!/bin/bash
sudo docker cp $(cat docker_id.txt):/opt/vosk-model-ru/model /media/alex/nvme-a/
python3 check_model.py test.wav /media/alex/nvme-a/model
