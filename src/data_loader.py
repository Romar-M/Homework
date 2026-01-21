import json
from models import Product, Category


def load_data_from_json(file_path: str) -> list:
    """
    Загружает данные из JSON файла и создает объекты Category и Product.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        list: Список объектов Category
    """
    categories = []

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for category_data in data:
            category = Category(
                name=category_data['name'],
                description=category_data['description'],
                products=[]  # Пустой список, будем добавлять через add_product
            )

            for product_data in category_data['products']:
                product = Product.new_product(product_data)  # Используем класс-метод
                category.add_product(product)

            categories.append(category)

    return categories