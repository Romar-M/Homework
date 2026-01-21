import pytest
import sys
from io import StringIO
from src.models import Product, Category


class TestProductPrivateAttributes:
    """Тесты для класса Product."""

    def test_price_is_private(self):
        """Тест, что атрибут цены приватный."""
        product = Product("Тест", "Описание", 100.0, 5)

        # Проверяем, что нельзя получить доступ напрямую
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_getter_returns_value(self):
        """Тест, что геттер price возвращает значение приватного атрибута."""
        product = Product("Тест", "Описание", 150.0, 3)
        assert product.price == 150.0

    def test_price_setter_valid_value(self):
        """Тест сеттера с валидным значением."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = 200.0
        assert product.price == 200.0

    def test_price_setter_zero_value(self, capsys):
        """Тест сеттера с нулевым значением."""
        product = Product("Тест", "Описание", 100.0, 5)

        product.price = 0

        # Проверяем сообщение
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

    def test_price_setter_negative_value(self, capsys):
        """Тест сеттера с отрицательным значением."""
        product = Product("Тест", "Описание", 100.0, 5)

        product.price = -50.0

        # Проверяем сообщение
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

    def test_new_product_classmethod(self):
        """Тест класс-метода new_product."""
        data = {
            "name": "Телефон",
            "description": "Смартфон",
            "price": 50000.0,
            "quantity": 10
        }

        product = Product.new_product(data)

        assert isinstance(product, Product)
        assert product.name == "Телефон"
        assert product.price == 50000.0
        assert product.quantity == 10


class TestCategoryPrivateAttributes:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сбрасываем счётчики перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_products_is_private(self):
        """Тест, что список товаров приватный."""
        category = Category("Тест", "Описание")

        with pytest.raises(AttributeError):
            _ = category.__products

    def test_add_product_method_exists(self):
        """Тест, что метод add_product существует."""
        category = Category("Тест", "Описание")
        assert hasattr(category, 'add_product')

    def test_add_product_increases_counter(self):
        """Тест, что add_product увеличивает счётчик продуктов."""
        category = Category("Тест", "Описание")
        product = Product("Товар", "Описание", 100.0, 5)

        initial_count = Category.product_count
        category.add_product(product)

        assert Category.product_count == initial_count + 1

    def test_products_getter_format(self):
        """Тест формата геттера products."""
        category = Category("Тест", "Описание")
        product1 = Product("Товар1", "Описание1", 100.0, 5)
        product2 = Product("Товар2", "Описание2", 200.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        result = category.products

        # Проверяем точный формат
        expected_line1 = "Товар1, 100.0 руб. Остаток: 5 шт."
        expected_line2 = "Товар2, 200.0 руб. Остаток: 3 шт."

        assert expected_line1 in result
        assert expected_line2 in result
        # Проверяем наличие переноса строки между товарами
        assert "\n" in result

    def test_products_getter_empty(self):
        """Тест геттера для пустой категории."""
        category = Category("Тест", "Описание")
        result = category.products
        assert result == ""  # Для пустого списка - пустая строка

    def test_init_with_products(self):
        """Тест инициализации категории с товарами."""
        product1 = Product("Товар1", "Описание1", 100.0, 2)
        product2 = Product("Товар2", "Описание2", 200.0, 3)

        category = Category("Тест", "Описание", [product1, product2])

        assert len(category) == 2
        assert Category.product_count == 2
        assert "Товар1, 100.0 руб. Остаток: 2 шт." in category.products


def test_category_count_increases():
    """Тест увеличения счётчика категорий."""
    Category.category_count = 0

    category1 = Category("Кат1", "Описание1")
    assert Category.category_count == 1

    category2 = Category("Кат2", "Описание2")
    assert Category.category_count == 2
