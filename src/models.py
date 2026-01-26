class Product:
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, product_data: dict):
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    def __str__(self):
        """Строковое представление продукта: Название продукта, X руб. Остаток: X шт."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Магический метод сложения.
        Возвращает сумму произведений цены на количество у двух объектов.
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")

        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = []

        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product):
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для приватного атрибута __products."""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result.rstrip()

    def __str__(self):
        """
        Строковое представление категории.
        Рассчитывает общее количество товаров на складе (quantity)
        для каждого продукта в приватном атрибуте products.
        """
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __len__(self):
        return len(self.__products)

    def get_products_list(self):
        """Возвращает список объектов продуктов."""
        return self.__products
