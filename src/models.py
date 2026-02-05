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
        # Сохраняем аргументы для вывода
        self._init_args = args
        self._init_kwargs = kwargs

        # Вызываем следующий __init__ в MRO
        if hasattr(super(), '__init__'):
            super().__init__(*args, **kwargs)

    def _log_creation(self):
        """Логирует создание объекта."""
        class_name = self.__class__.__name__
        args_str = ", ".join([repr(arg) for arg in self._init_args])
        print(f"{class_name}({args_str})")


class Product(LogCreationMixin, BaseProduct):
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Сохраняем атрибуты напрямую (не через property в __init__)
        self._name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

        # Инициализируем миксин
        super().__init__(name, description, price, quantity)

        # Логируем создание
        self._log_creation()

    @property
    def name(self):
        """Геттер для названия."""
        return self._name

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Сеттер для цены с проверкой."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

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
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Магический метод сложения с проверкой типов."""
        if type(self) != type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return (self.price * self.quantity) + (other.price * other.quantity)

    def __repr__(self):
        """Представление для отладки."""
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        # Сохраняем дополнительные атрибуты
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

        # Вызываем родительский __init__
        super().__init__(name, description, price, quantity)

    def __repr__(self):
        """Представление для отладки."""
        return (f"Smartphone('{self.name}', '{self.description}', {self.price}, "
                f"{self.quantity}, {self.efficiency}, '{self.model}', "
                f"{self.memory}, '{self.color}')")


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        # Сохраняем дополнительные атрибуты
        self.country = country
        self.germination_period = germination_period
        self.color = color

        # Вызываем родительский __init__
        super().__init__(name, description, price, quantity)

    def __repr__(self):
        """Представление для отладки."""
        return (f"LawnGrass('{self.name}', '{self.description}', {self.price}, "
                f"{self.quantity}, '{self.country}', '{self.germination_period}', "
                f"'{self.color}')")


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
        """Добавляет продукт в категорию."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследники")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для списка товаров."""
        result = ""
        for product in self.__products:
            result += str(product) + "\n"
        return result.rstrip()

    def __str__(self):
        """Строковое представление категории."""
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __len__(self):
        """Возвращает количество товаров в категории."""
        return len(self.__products)

    def get_products_list(self):
        """Возвращает список объектов продуктов."""
        return self.__products
