import pytest
from src.models import Product, Category


class TestProductMagicMethods:
    """Тесты магических методов класса Product."""

    def test_product_str_method(self):
        """Тест метода __str__ для Product."""
        product = Product("Телефон", "Смартфон", 50000.0, 10)
        expected = "Телефон, 50000.0 руб. Остаток: 10 шт."
        assert str(product) == expected

    def test_product_add_method_valid(self):
        """Тест метода __add__ для двух продуктов."""
        product1 = Product("Товар1", "Описание1", 100.0, 10)  # 100 * 10 = 1000
        product2 = Product("Товар2", "Описание2", 200.0, 5)  # 200 * 5 = 1000
        result = product1 + product2
        assert result == 2000.0

    def test_product_add_method_commutative(self):
        """Тест коммутативности сложения."""
        product1 = Product("Товар1", "Описание1", 100.0, 2)
        product2 = Product("Товар2", "Описание2", 50.0, 4)
        assert product1 + product2 == product2 + product1
        assert product1 + product2 == 400.0  # 100*2 + 50*4

    def test_product_add_method_invalid_type(self):
        """Тест метода __add__ с неправильным типом."""
        product = Product("Товар", "Описание", 100.0, 5)
        with pytest.raises(TypeError, match="Можно складывать только объекты Product"):
            product + "не продукт"

    def test_product_str_includes_all_info(self):
        """Тест, что __str__ включает всю необходимую информацию."""
        product = Product("Тестовый", "Тест", 123.45, 7)
        result = str(product)
        assert "Тестовый" in result
        assert "123.45" in result
        assert "7" in result
        assert "руб." in result
        assert "Остаток:" in result


class TestCategoryMagicMethods:
    """Тесты магических методов класса Category."""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_category_str_method(self):
        """Тест метода __str__ для Category."""
        product1 = Product("Товар1", "Описание1", 100.0, 3)
        product2 = Product("Товар2", "Описание2", 200.0, 2)

        category = Category("Тестовая категория", "Описание", [product1, product2])

        expected = "Тестовая категория, количество продуктов: 5 шт."
        assert str(category) == expected

    def test_category_str_method_empty(self):
        """Тест метода __str__ для пустой категории."""
        category = Category("Пустая категория", "Описание")
        expected = "Пустая категория, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_category_str_calculates_total_quantity(self):
        """Тест, что __str__ рассчитывает общее количество товаров."""
        product1 = Product("Товар1", "Описание1", 100.0, 10)
        product2 = Product("Товар2", "Описание2", 200.0, 20)
        product3 = Product("Товар3", "Описание3", 300.0, 30)

        category = Category("Тест", "Описание", [product1, product2, product3])

        total_quantity = 10 + 20 + 30
        expected = f"Тест, количество продуктов: {total_quantity} шт."
        assert str(category) == expected

    def test_category_products_uses_product_str(self):
        """Тест, что геттер products использует __str__ продуктов."""
        product = Product("Тестовый товар", "Описание", 100.0, 5)
        category = Category("Тест", "Описание", [product])

        products_str = category.products
        expected = "Тестовый товар, 100.0 руб. Остаток: 5 шт."
        assert products_str == expected


class TestIntegration:
    """Интеграционные тесты."""

    def test_main_example_works(self):
        """Тест, что пример из main работает корректно."""
        product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

        # Проверяем __str__ продуктов
        assert "Samsung Galaxy S23 Ultra" in str(product1)
        assert "180000.0" in str(product1)
        assert "5" in str(product1)

        # Создаем категорию
        category = Category(
            "Смартфоны",
            "Описание",
            [product1, product2, product3]
        )

        # Проверяем __str__ категории
        total_quantity = 5 + 8 + 14
        expected_category_str = f"Смартфоны, количество продуктов: {total_quantity} шт."
        assert str(category) == expected_category_str

        # Проверяем сложение
        result1 = product1 + product2
        expected1 = (180000.0 * 5) + (210000.0 * 8)
        assert result1 == expected1

        result2 = product1 + product3
        expected2 = (180000.0 * 5) + (31000.0 * 14)
        assert result2 == expected2

    def test_products_getter_format(self):
        """Тест формата геттера products."""
        product1 = Product("Товар1", "Описание1", 100.0, 1)
        product2 = Product("Товар2", "Описание2", 200.0, 2)

        category = Category("Тест", "Описание", [product1, product2])

        products_str = category.products
        lines = products_str.split('\n')

        assert len(lines) == 2
        assert lines[0] == "Товар1, 100.0 руб. Остаток: 1 шт."
        assert lines[1] == "Товар2, 200.0 руб. Остаток: 2 шт."


def test_existing_functionality_still_works():
    """Тест, что существующая функциональность по-прежнему работает."""
    # Проверяем приватный атрибут цены
    product = Product("Тест", "Описание", 100.0, 5)
    with pytest.raises(AttributeError):
        _ = product.__price

    # Проверяем геттер и сеттер
    assert product.price == 100.0
    product.price = 150.0
    assert product.price == 150.0

    # Проверяем валидацию цены
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    product.price = -50

    output = sys.stdout.getvalue()
    sys.stdout = old_stdout

    assert "Цена не должна быть нулевая или отрицательная" in output
    assert product.price == 150.0  # Цена не изменилась

    # Проверяем класс-метод
    product_data = {
        "name": "Новый товар",
        "description": "Описание",
        "price": 200.0,
        "quantity": 3
    }
    new_product = Product.new_product(product_data)
    assert new_product.name == "Новый товар"
    assert new_product.price == 200.0
    assert new_product.quantity == 3

    # Проверяем приватный список товаров в категории
    category = Category("Тест", "Описание")
    with pytest.raises(AttributeError):
        _ = category.__products

    # Проверяем add_product и счетчики
    initial_count = Category.product_count
    category.add_product(product)
    assert Category.product_count == initial_count + 1
    assert len(category) == 1
