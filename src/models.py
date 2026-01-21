class Product:
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # ПРИВАТНЫЙ атрибут (два подчёркивания!)
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены. Возвращает значение приватного атрибута."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Сеттер для цены с проверкой на положительное значение."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, product_data: dict):
        """
        Класс-метод для создания продукта из словаря.

        Args:
            product_data: Словарь с ключами: name, description, price, quantity

        Returns:
            Product: Экземпляр класса Product
        """
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )


class Category:
    """Класс для представления категории товаров."""

    # Класс-атрибуты
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = []  # ПРИВАТНЫЙ атрибут (два подчёркивания!)

        # Увеличиваем счётчик категорий
        Category.category_count += 1

        # Добавляем товары, если они переданы
        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product):
        """
        Добавляет продукт в приватный атрибут __products.

        Args:
            product: Объект класса Product
        """
        self.__products.append(product)
        Category.product_count += 1  # Увеличиваем счётчик продуктов на 1

    @property
    def products(self):
        """
        Геттер для приватного атрибута __products.

        Returns:
            str: Строка со всеми продуктами по шаблону
        """
        result = ""
        for product in self.__products:
            # Строгий шаблон: "Название продукта, X руб. Остаток: X шт.\n"
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result.rstrip()  # Убираем последний перенос строки

    def __len__(self):
        """Возвращает количество товаров в категории."""
        return len(self.__products)
