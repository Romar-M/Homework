import pytest
from src.models import Product, Category


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Тест корректности инициализации объекта Product."""
        product = Product(
            name="Test Product",
            description="Test Description",
            price=1000.0,
            quantity=10
        )

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 1000.0
        assert product.quantity == 10

    def test_product_attributes_types(self):
        """Тест типов атрибутов Product."""
        product = Product("Test", "Desc", 100.0, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)


class TestCategory:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сбрасываем счетчики перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Тест корректности инициализации объекта Category."""
        product1 = Product("P1", "Desc1", 100.0, 1)
        product2 = Product("P2", "Desc2", 200.0, 2)

        category = Category(
            name="Test Category",
            description="Test Description",
            products=[product1, product2]
        )

        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert len(category.products) == 2
        assert category.products[0].name == "P1"

    def test_category_count(self):
        """Тест подсчета количества категорий."""
        # До создания категорий
        assert Category.category_count == 0

        # Создаем первую категорию
        category1 = Category("Cat1", "Desc1", [])
        assert Category.category_count == 1

        # Создаем вторую категорию
        category2 = Category("Cat2", "Desc2", [])
        assert Category.category_count == 2

    def test_product_count(self):
        """Тест подсчета количества продуктов."""
        # До создания категорий
        assert Category.product_count == 0

        # Создаем категорию с 3 продуктами
        products = [
            Product("P1", "Desc1", 100.0, 1),
            Product("P2", "Desc2", 200.0, 2),
            Product("P3", "Desc3", 300.0, 3)
        ]
        category1 = Category("Cat1", "Desc1", products)
        assert Category.product_count == 3

        # Создаем вторую категорию с 2 продуктами
        products2 = [
            Product("P4", "Desc4", 400.0, 4),
            Product("P5", "Desc5", 500.0, 5)
        ]
        category2 = Category("Cat2", "Desc2", products2)
        assert Category.product_count == 5

    def test_category_attributes_types(self):
        """Тест типов атрибутов Category."""
        category = Category("Test", "Desc", [])

        assert isinstance(category.name, str)
        assert isinstance(category.description, str)
        assert isinstance(category.products, list)
