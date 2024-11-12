# LUMathMate_bot
Этот телеграм-бот будет вашим помощником в преподавании и обучении математике.

Его основная функция - упростить процесс взаимодействия между учеником и учителем, а именно передачу конспектов, дополнительных материалов, домашних заданий, отслеживании прогресса и других опций.

Статус разработки: в разработке 

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Разработка](#разработка)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [python 3.10](https://www.python.org/downloads/release/python-3100/)
- [aiogram 3.13](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://docs.aiogram.dev/uk-ua/latest/&ved=2ahUKEwiQnInozNaJAxVocfEDHcHeLW0QFnoECBgQAQ&usg=AOvVaw2426AC47_6UBPQDZT57rdj)
- [PostgreSQL](https://www.postgresql.org/)
- [PlantUML](https://plantuml.com/)

## Использование
К сожалению, на данном этапе разработки бот не доступен в общем доступе. Но совсем скоро он будет запущен на сервере, и вы сможете написать ему в [телеграме](https://t.me/lumathmate_bot).

## Разработка
### Требования
Для работы проекта, необходимы библиотеки [aiogram 3.13](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://docs.aiogram.dev/uk-ua/latest/&ved=2ahUKEwiQnInozNaJAxVocfEDHcHeLW0QFnoECBgQAQ&usg=AOvVaw2426AC47_6UBPQDZT57rdj), [psycopg2](https://pypi.org/project/psycopg2/)
Для работы с UML-графами, необходим [Graphviz](https://graphviz.org/) и [PlantUML-плагин](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml) (для [VSCode](https://code.visualstudio.com/)).

### Установка зависимостей
Для установки зависимостей, выполните команду:
```
$ pip install -r requirements.txt 
``` 

### Инициализация бота
Для инициализации бота, выполните команды (Linux):
```
mkdir config
cd config 
echo "[Bot]" >> bot.ini
echo "token=<YOUR-TGBOT-TOKEN>" >> bot.ini 
```

### Инициализация базы данных
Для инициализации базы данных, выполните команды (Linux):
```
cd config
echo "[postgresql]" >> database.ini
echo "host = <YOUR-HOST>" >> database.ini
echo "database = <YOUR-DATABASE-NAME>" >> database.ini
echo "user = <YOUR-USERNAME>" >> database.ini
echo "password = <YOUR-PASSWORD>" >> database.ini
```
Описание структуры базы данных вы сможете найти позже в директории "uml".

## To do
- [x] Реализовать авторизацию 
- [x] Реализовать функцию отправки конспекта учителем
- [x] Реализовать функцию получения конспекта учеником
- [ ] Добавить возможность добавлять новых учеников
- [ ] Добавить возможность отправлять домашние задания
- [ ] Добавить возможность отслеживания статистики
- [ ] Добавить возможность администрирования группой
- [ ] Добавить мини-игры и тренировки простых упражнений

## Команда проекта
- [Ли Любовь](https://t.me/empty_space1310) - автор идеи и разработчик