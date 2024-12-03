import argparse
import json
import csv
import os
from collections import defaultdict
from datetime import datetime

def load_json_files(directory_path):
    """
    Загружает данные из всех JSON-файлов в указанной директории.
    Предполагается, что каждый отзыв находится на отдельной строке.
    """
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            print(f"Загрузка данных из файла: {filename}")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        print(f"Предупреждение: Некорректный JSON в файле {filename} на строке {line_number}. Пропуск.")
                        continue  # Пропускаем строки, которые не являются корректным JSON

def list_products_by_popularity(data):
    """
    Создаёт список продуктов, отсортированных по популярности (количеству отзывов).
    Сохраняет результат в 'products_by_popularity.csv'.
    """
    popularity = defaultdict(int)
    total_reviews = 0
    for review in data:
        total_reviews += 1
        product = review.get('asin')
        if product:
            popularity[product] += 1
    sorted_popularity = sorted(popularity.items(), key=lambda x: x[1], reverse=True)
    with open('products_by_popularity.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Product ID', 'Number of Reviews'])
        writer.writerows(sorted_popularity)
    print(f"Обработано {total_reviews} отзывов.")
    print("Список продуктов по популярности сохранен в 'products_by_popularity.csv'")

def list_products_by_rating(data):
    """
    Создаёт список продуктов, отсортированных по рейтингу (с учётом веса отзыва).
    Сохраняет результат в 'products_by_rating.csv'.
    """
    ratings = defaultdict(lambda: {'total': 0, 'count': 0})
    processed_reviews = 0
    for review in data:
        product = review.get('asin')
        if not product:
            continue
        rating = review.get('overall')
        if not isinstance(rating, (int, float)):
            continue
        helpful = 1  # По умолчанию вес равен 1
        if 'helpful' in review:
            helpful_votes = review.get('helpful')
            if isinstance(helpful_votes, list) and len(helpful_votes) >= 1:
                try:
                    helpful = int(helpful_votes[0])
                    if helpful < 0:
                        helpful = 1
                except (ValueError, TypeError):
                    helpful = 1
        ratings[product]['total'] += rating * helpful
        ratings[product]['count'] += helpful
        processed_reviews += 1
    average_ratings = [
        (product, round(ratings[product]['total'] / ratings[product]['count'], 2) if ratings[product]['count'] else 0)
        for product in ratings
    ]
    sorted_ratings = sorted(average_ratings, key=lambda x: x[1], reverse=True)
    with open('products_by_rating.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Product ID', 'Average Rating'])
        writer.writerows(sorted_ratings)
    print(f"Обработано {processed_reviews} отзывов для расчёта рейтингов.")
    print("Список продуктов по рейтингу сохранен в 'products_by_rating.csv'")

def most_popular_products_period(data, start_date, end_date):
    """
    Создаёт список самых популярных продуктов за указанный период.
    Сохраняет результат в 'most_popular_products_period.csv'.
    """
    popularity = defaultdict(int)
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("Неверный формат даты. Используйте YYYY-MM-DD.")
        return

    matched_reviews = 0
    for review in data:
        product = review.get('asin')
        if not product:
            continue
        unix_time = review.get('unixReviewTime')
        if not isinstance(unix_time, int):
            continue
        try:
            date = datetime.fromtimestamp(unix_time)
            if start <= date <= end:
                popularity[product] += 1
                matched_reviews += 1
        except (ValueError, OSError):
            continue  # Пропускаем некорректные даты

    if matched_reviews == 0:
        print(f"Нет отзывов в указанном диапазоне с {start_date} по {end_date}.")
    else:
        sorted_popularity = sorted(popularity.items(), key=lambda x: x[1], reverse=True)
        with open('most_popular_products_period.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Product ID', 'Number of Reviews'])
            writer.writerows(sorted_popularity)
        print(f"Обработано {matched_reviews} отзывов за период с {start_date} по {end_date}.")
        print("Самые популярные продукты за период сохранены в 'most_popular_products_period.csv'")

def search_reviews(data, search_text):
    """
    Ищет отзывы, содержащие заданный текст.
    Сохраняет результат в 'search_results.csv'.
    """
    results = []
    matched_reviews = 0
    for review in data:
        review_text = review.get('reviewText') or review.get('reviewContent') or review.get('body')
        if review_text and search_text.lower() in review_text.lower():
            product = review.get('asin')
            results.append((product, review_text))
            matched_reviews += 1
    if matched_reviews == 0:
        print(f"По вашему запросу '{search_text}' не найдено ни одного отзыва.")
    else:
        with open('search_results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Product ID', 'Review Text'])
            writer.writerows(results)
        print(f"Найдено {matched_reviews} отзывов, содержащих текст '{search_text}'.")
        print("Результаты поиска сохранены в 'search_results.csv'")

def main():
    parser = argparse.ArgumentParser(description='Консольный парсер отзывов Amazon')
    parser.add_argument('directory_path', type=str, help='Путь к директории с JSON-файлами отзывов')
    parser.add_argument('--start_date', type=str, help='Начальная дата для периода (YYYY-MM-DD)', default='2000-01-01')
    parser.add_argument('--end_date', type=str, help='Конечная дата для периода (YYYY-MM-DD)', default='2030-12-31')
    parser.add_argument('--search_text', type=str, help='Текст для поиска в отзывах', default='')

    args = parser.parse_args()

    if not os.path.isdir(args.directory_path):
        print(f"Ошибка: Путь '{args.directory_path}' не является директорией или не существует.")
        return

    print("Загрузка данных из всех JSON-файлов...")
    data = load_json_files(args.directory_path)

    # Преобразуем генератор в список для многократного прохода по данным
    data = list(data)
    print(f"Всего загружено {len(data)} отзывов.")

    if len(data) == 0:
        print("Нет данных для анализа.")
        return

    print("\nАнализ данных по популярности продуктов...")
    list_products_by_popularity(data)

    print("\nАнализ данных по рейтингу продуктов...")
    list_products_by_rating(data)

    print(f"\nАнализ самых популярных продуктов за период с {args.start_date} по {args.end_date}...")
    most_popular_products_period(data, args.start_date, args.end_date)

    if args.search_text:
        print(f"\nПоиск отзывов, содержащих текст: '{args.search_text}'...")
        search_reviews(data, args.search_text)

if __name__ == "__main__":
    main()
