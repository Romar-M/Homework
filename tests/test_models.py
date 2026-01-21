import pytest
import io
import sys
from src.models import Product, Category


def test_add_product_method():
    """Тест метода add_product."""
    category = Category("Тест", "Описание")
    product = Product("Товар", "Описание", 100.0, 5)

    # Проверяем, что метод существует
    assert hasattr(category, 'add_product'), "Метод add_product отсутствует"

    # Проверяем добавление
    initial_count = Category.product_count
    category.add_product(product)

    assert len(category) == 1
    assert Category.product_count == initial_count + 1


def test_products_getter_format():
    """Тест формата вывода геттера products."""
    category = Category("Тест", "Описание")
    product = Product("Телефон", "Смартфон", 50000.0, 3)

    category.add_product(product)
    result = category.products

    # Проверяем формат
    assert "Телефон, 50000.0 руб. Остаток: 3 шт." in result
    assert result.endswith("3 шт.") or "\n" in result


def test_price_setter_validation():
    """Тест валидации в сеттере цены."""
    product = Product("Тест", "Описание", 100.0, 5)

    # Перехватываем вывод
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    # Пытаемся установить отрицательную цену
    product.price = -50

    output = sys.stdout.getvalue()
    sys.stdout = old_stdout

    assert "Цена не должна быть нулевая или отрицательная" in output
    assert product.price == 100.0  # Цена не изменилась


def test_new_product_classmethod():
    """Тест класс-метода new_product."""
    product_data = {
        "name": "Новый товар",
        "description": "Описание",
        "price": 1000.0,
        "quantity": 7
    }

    product = Product.new_product(product_data)

    assert isinstance(product, Product)
    assert product.name == "Новый товар"
    assert product.price == 1000.0
    assert product.quantity == 7


def test_private_products_attribute():
    """Тест, что атрибут products приватный."""
    category = Category("Тест", "Описание")

    # Не должно быть прямого доступа
    with pytest.raises(AttributeError):
        _ = category.__products

    # Но должен быть доступ через геттер
    assert hasattr(category, 'products')
    result = category.products
    assert isinstance(result, str)


def test_category_initialization_with_products():
    """Тест инициализации категории с продуктами."""
    product1 = Product("Товар1", "Описание1", 100.0, 2)
    product2 = Product("Товар2", "Описание2", 200.0, 3)

    category = Category("Тест", "Описание", [product1, product2])

    assert len(category) == 2
    assert "Товар1, 100.0 руб. Остаток: 2 шт." in category.products
    assert "Товар2, 200.0 руб. Остаток: 3 шт." in category.products
