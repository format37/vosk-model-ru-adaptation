## Источник:

https://github.com/va-stepanov/vosk-model-ru-adaptation

## Цель

Расширить, адаптировать словарь имеющейся модели для улучшения качества распознавания речи.

## Подготовка

Убедимся что модель не распознает контрольное слово. Запишем файл, в котором помимо знакомых для модели слов, фигурируют незнакомые. Я записал фразу 'машина приехала на улицу чоботовская и остановилась' в файл test.wav. Новое слово - чоботовская.


Собираем и запускаем контейнер, в котором будут готовиться и добавляться слова
```
git clone https://github.com/va-stepanov/vosk-model-ru-adaptation.git
cd vosk-model-ru-adaptation
sudo docker build --file Dockerfile.kaldi-vosk-model-ru --tag alphacep/kaldi-vosk-model-ru:latest .
sudo docker run -d -p 2700:2700 alphacep/kaldi-vosk-model-ru:latest
```
Полученный идентификатор контейнера помещаем в переменную (идентификатор заменить на свой):
```
export VOSKID=a2c164cdba01d0d9a9d33482f2bdfaa6743b40831dbfcd3eedb9febc4b954482
```
## Добавление слов в модель

Подготавливаем corpus.txt, в котором вводим по предложению на строку или слово на строку  
Отправляем corpus.txt с хоста на контейрер:
```
sudo docker cp ./corpus.txt $VOSKID:/opt/vosk-model-ru/model/new/data/corpus
```
После отправки файла начнется процесс добавления слов в модель. Следить за ним можно по нагрузке на процессор, или через мониторинг portainer'a. Когда нагрузка резко спадет - модель готова, можно скачивать:

## Копирование модели на хост
```
sudo docker cp $VOSKID:/opt/vosk-model-ru/model .
```
