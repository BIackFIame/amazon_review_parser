# Amazon Reviews Parser

**Консольный парсер для обработки JSON-файлов с отзывами о продуктах Amazon.**

## Описание

Этот проект представляет собой консольный парсер, который обрабатывает JSON-файлы с отзывами о продуктах Amazon. Парсер выполняет следующие задачи:

- **Список продуктов от самого популярного**: Определяет продукты с наибольшим количеством отзывов.
- **Список продуктов по рейтингу**: Рассчитывает средний рейтинг продуктов, учитывая вес отзывов.
- **Самые популярные товары за период**: Выводит список самых популярных продуктов за указанный период.
- **Поиск отзывов по тексту**: Позволяет искать отзывы, содержащие определённый текст.

Результаты работы программы сохраняются в виде CSV-файлов.


## Требования

- **Python**: Версия 3.6 или выше.
- **Библиотеки Python**: Используются стандартные библиотеки (`argparse`, `json`, `csv`, `os`, `collections`, `datetime`).

## Установка

1. **Установка Python**:

    - **Windows**:
        - Скачайте установщик Python с [официального сайта](https://www.python.org/downloads/windows/).
        - Запустите установщик и следуйте инструкциям. Не забудьте отметить опцию "Add Python to PATH".

    - **macOS**:
        - Скачайте установщик Python с [официального сайта](https://www.python.org/downloads/mac-osx/).
        - Запустите установщик и следуйте инструкциям.

    - **Linux**:
        - Используйте менеджер пакетов вашей дистрибуции. Например, для Debian/Ubuntu:
            ```bash
            sudo apt-get update
            sudo apt-get install python3
            ```

2. **Клонирование Репозитория**:

    Если вы ещё не создали локальный репозиторий, выполните следующие шаги:

    ```bash
    git clone https://github.com/ВАШЕ_ИМЯ_ПОЛЬЗОВАТЕЛЯ/amazon-reviews-parser.git
    cd amazon-reviews-parser
    ```

    *Замените `ВАШЕ_ИМЯ_ПОЛЬЗОВАТЕЛЯ` на ваш реальный логин GitHub.*

3. **Установка Зависимостей**:

    Для данного скрипта дополнительные зависимости не требуются, так как используются только стандартные библиотеки Python.

## Использование

### Предположения

- Все JSON-файлы с отзывами находятся в одной директории вместе с `amazon_reviews_parser.py`.
- Каждый отзыв представлен в виде отдельной строки в JSON-файле.

### Запуск Скрипта

Откройте терминал (или командную строку) и перейдите в директорию проекта:

- **Windows**:

    ```bash
    cd %USERPROFILE%\Desktop\amazon_reviews_parser
    ```

- **macOS/Linux**:

    ```bash
    cd ~/Desktop/amazon_reviews_parser
    ```

#### Основная Команда

```bash
python amazon_reviews_parser.py . [опции]
```

. указывает на текущую директорию, где находятся ваши JSON-файлы и скрипт.
Опции
--start_date YYYY-MM-DD: Начальная дата для анализа самых популярных продуктов за период. По умолчанию 2000-01-01.
--end_date YYYY-MM-DD: Конечная дата для анализа самых популярных продуктов за период. По умолчанию 2030-12-31.
--search_text "текст для поиска": Текст, который вы хотите найти в отзывах.

Примеры Команд

Поиск отзывов, содержащих слово "great":
```bash
python amazon_reviews_parser.py . --search_text "great"
```

Анализ самых популярных продуктов за период с 2010-01-01 по 2018-12-31:
```bash
python amazon_reviews_parser.py . --start_date 2010-01-01 --end_date 2018-12-31
```

Комбинированный анализ с поиском и периодом:
```bash
python amazon_reviews_parser.py . --start_date 2010-01-01 --end_date 2018-12-31 --search_text "great"
```