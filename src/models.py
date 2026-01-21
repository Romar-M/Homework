class Product:
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер для цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return  # Не меняем цену
        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict):
        """Класс-метод для создания продукта из словаря."""
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class Category:
    """Класс для представления категории товаров."""

    category_count = 0  # Количество категорий
    product_count = 0  # Количество товаров

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = []  # ПРИВАТНЫЙ атрибут

        # Добавляем продукты через метод add_product
        if products:
            for product in products:
                self.add_product(product)

        Category.category_count += 1

    def add_product(self, product):
        """Добавляет продукт в приватный список продуктов."""
        self.__products.append(product)
        Category.product_count += 1  # Увеличиваем счетчик товаров

    @property
    def products(self):
        """Геттер, возвращающий строку с информацией о товарах."""
        if not self.__products:
            return "В этой категории пока нет товаров."

        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result.strip()

    def get_products_list(self):
        """Вспомогательный метод для получения списка объектов."""
        return self.__products

    def __len__(self):
        return len(self.__products)

    def __repr__(self):
        return f"Category(name='{self.name}', products_count={len(self)})"
