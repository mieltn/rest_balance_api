# REST Balance API
API имеет 3 основных метода:
- получение баланса пользователя
- обновление баланса (списание/зачисление)
- перевод денег от пользователя к пользователю

Для вспомогательных целей есть функция добавления нового пользователя.

Чтобы запустить сервер API необходимо (приведены команды для Unix/Linux):
1. Иметь установленный Python и git
2. Клонировать репозиторий `git clone https://github.com/mieltn/rest_balance_api.git`
3. Установить необходимые модули `pip install -r requirements.txt`
4. Записать в переменную основной файл приложения `export FLASK_APP=app.py`
5. Запустить сервер `flask run`

Для тестирования можно использовать файл <i>testing.py</i>. В нём в виде функций реализованы все основные варианты запросов к API.

Получить баланс пользователя можно в разных валютах. Для этого к url запроса добавляется параметр `?currency=<CURRENCY-OF-INTEREST>`. Для конвертации используется [данное API](https://freecurrencyapi.net/). Чтобы работало нужно зарегистрироваться и вставить полученный токен в <i>urls.py</i>.

<!-- There are three main methods:
- getting balance
- updating balance (decreasing or increasing)
- adding new transaction

For subsidary needs API could add new clients.

To run API ... -->