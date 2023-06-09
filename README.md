# Сравниваем вакансии программистов

Скрипт получает данные о вакансиях с сайтов [HeadHunter](https://hh.ru) и [SuperJob](https://api.superjob.ru/). А также
выводит информацию по средним зарплатам для различных языков программирования по Москве.


### Как установить

Для начала работы необходимо:
* Зарегистрировать приложение на сайте [SuperJob](https://api.superjob.ru/register), сайт приложения можно указать любой
* Получить Secret key приложения 
* В папке со скриптом создать файл `.env` и записать в него Secret key в виде:
```
SUPERJOB_TOKEN=Ваш ключ
```
[Python3](https://www.python.org/downloads/) должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Как использовать
Запустите скрипт с помощью команды
```
 python main.py
```
Получение данных занимает некоторое время, возможно придется подождать до 5 мин.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
