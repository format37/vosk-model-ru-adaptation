#### Автоматическое пополнение словаря пользовательскими словами
В пайплайне автоматического обновления словаря, перед сборкой corpus.txt, следует иметь актуальный словарь из текущей модели. Он будет использоваться в скрипте для исключения из corpus.txt слов, которые уже есть в модели.   
Добавим в cron удаление прежнего и скачивание актуального словаря. Каждый день в 02:58 и 02:59.   
```
sudo su
crontab -e
```
Путь абсолютьный, у каждого он свой. Поверьте, что бы у вас пути и имя контейнера были корректны.
```
58 2 * * * if [ -f "/home/alex/projects/vosk-model-ru-adaptation/model_files/words.txt" ]; then rm -r /home/alex/projects/vosk-model-ru-adaptation/model_files/words.txt; fi
59 2 * * * docker cp vosk-model-ru-adaptation_server_x_1:/opt/vosk-model-ru/model/graph/words.txt /home/alex/projects/vosk-model-ru-adaptation/model_files/
```