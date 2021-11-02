#### Автоматическое пополнение словаря пользовательскими словами
В пайплайне автоматического обновления словаря, перед сборкой corpus.txt, следует иметь актуальный словарь из текущей модели. Он будет использоваться в скрипте для исключения из corpus.txt слов, которые уже есть в модели.   
Добавим в cron удаление прежнего и скачивание актуального словаря. Каждый день в 2:59.   
```
crontab -e
```
Путь абсолютьный, у каждого он свой. Поверьте, что бы у вас пути и название контейнера был корректны.
```
59 2 * * * if [ -f "/home/alex/rig1/projects/pc/vosk-model-ru-adaptation/model_files/words.txt" ]; then rm -r /home/alex/rig1/projects/pc/vosk-model-ru-adaptation/model_files/words.txt; fi ;/usr/bin/docker cp vosk-model-ru-adaptation_server_1:/opt/vosk-model-ru/model/graph/words.txt /home/alex/rig1/projects/pc/vosk-model-ru-adaptation/model_files/
```