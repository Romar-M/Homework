from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def price(self):
        pass


class LogCreationMixin:
    """Миксин для логирования создания объектов."""

    def __init__(self, *args, **kwargs):
        # Вызываем super().__init__ только если есть родительский класс с __init__
        if hasattr(super(), '__init__'):
            super().__init__(*args, **kwargs)

        # Получаем имя класса
        class_name = self.__class__.__name__

        # Формируем аргументы для вывода
        if class_name == 'Product':
            name, description, price, quantity = args
            print(f"{class_name}('{name}', '{description}', {price}, {quantity})")
        elif class_name == 'Smartphone':
            name, description, price, quantity, efficiency, model, memory, color = args
            print(
                f"{class_name}('{name}', '{description}', {price}, {quantity}, {efficiency}, '{model}', {memory}, '{color}')")
        elif class_name == 'LawnGrass':
            name, description, price, quantity, country, germination_period, color = args
            print(
                f"{class_name}('{name}', '{description}', {price}, {quantity}, '{country}', '{germination_period}', '{color}')")


class Product(BaseProduct, LogCreationMixin):
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

        # Инициализация миксина
        super().__init__(name, description, price, quantity)

    @property
    def name(self):
        return self._name if hasattr(self, '_name') else self.name

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
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return (self.price * self.quantity) + (other.price * other.quantity)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self):
        return f"Smartphone('{self.name}', '{self.description}', {self.price}, {self.quantity}, {self.efficiency}, '{self.model}', {self.memory}, '{self.color}')"


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self):
        return f"LawnGrass('{self.name}', '{self.description}', {self.price}, {self.quantity}, '{self.country}', '{self.germination_period}', '{self.color}')"


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
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследники")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result.rstrip()

    def __str__(self):
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __len__(self):
        return len(self.__products)

    def get_products_list(self):
        return self.__products
