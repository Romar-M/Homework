import json
from models import Product, Category


def load_data_from_json(file_path: str) -> list:
    """
    Загружает данные из JSON файла и создает объекты Category и Product.
    """
    categories = []

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for category_data in data:
            # Создаём категорию БЕЗ товаров
            category = Category(
                name=category_data['name'],
                description=category_data['description']
            )

            # Добавляем товары через метод add_product
            for product_data in category_data['products']:
                # Используем класс-метод для создания продукта
                product = Product.new_product(product_data)
                category.add_product(product)

            categories.append(category)

    return categories
