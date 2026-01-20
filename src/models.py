class Product:
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация товара.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество товара в наличии
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для представления категории товаров."""

    # Атрибуты класса
    category_count = 0  # Количество категорий
    product_count = 0  # Количество товаров

    def __init__(self, name: str, description: str, products: list):
        """
        Инициализация категории.

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров (объектов Product) в категории
        """
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счетчики
        Category.category_count += 1
        Category.product_count += len(products)
