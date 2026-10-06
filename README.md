# Курси валют ПриватБанку

Консольна утиліта та websocket-чат, які отримують курси валют із [публічного API ПриватБанку](https://api.privatbank.ua/#p24/exchangeArchive) (архів курсів).

Репозиторій: https://github.com/Kuzminyo/hw_sw_5.git

## Встановлення

Потрібен Python 3.10+.

```
git clone https://github.com/Kuzminyo/hw_sw_5.git
cd hw_sw_5
pip install -r requirements.txt
```

## Консольна утиліта

```
python main.py <days> [-c CODE [CODE ...]]
```

- `days` — кількість днів (від 1 до 10), починаючи з сьогодні.
- `-c`, `--currency` — додаткові валюти до EUR і USD.

Приклади:

```
python main.py 2
python main.py 3 -c CHF PLN
```

Результат — JSON, найновіша дата першою:

```
[
  {
    "06.10.2026": {
      "EUR": {"sale": 50.85, "purchase": 49.85},
      "USD": {"sale": 45.2, "purchase": 44.6}
    }
  }
]
```

Якщо `days` поза діапазоном 1–10 або виникла мережева помилка, утиліта виводить повідомлення `Error: ...` у stderr і завершується з кодом 1.

## Чат

1. Запустіть сервер (`ws://localhost:8765`):

   ```
   python -m chat.server
   ```

2. У окремих терміналах запустіть клієнтів і введіть ім'я:

   ```
   python -m chat.client
   ```

Звичайні повідомлення розсилаються всім учасникам. Команда `exchange` показує курси валют усім у чаті:

| Команда | Результат |
|---|---|
| `exchange` | курс на сьогодні |
| `exchange 2` | курс за останні 2 дні |
| `exchange 2 chf pln` | те саме з додатковими валютами |

Кожне виконання `exchange` записується у файл `exchange_commands.log` (час, ім'я користувача, команда).

## Структура

```
main.py              CLI
exchange/
  source.py          інтерфейс джерела курсів (RateSource)
  privatbank.py      реалізація на aiohttp
  service.py         логіка днів і ліміт 10 днів
  formatters.py      JSON- і текстове форматування
  runner.py          створення сесії та отримання курсів
  models.py, errors.py
chat/
  server.py          websocket-сервер
  client.py          консольний клієнт
  commands.py        обробка команди exchange
  exchange_log.py    логування у файл (aiofile + aiopath)
```
