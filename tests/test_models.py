import pytest
from src.models import Product, Category, ZeroQuantityError, Smartphone, LawnGrass


def test_product_zero_quantity_raises_error():
    """Тест создания товара с нулевым количеством вызывает ошибку."""
    with pytest.raises(ZeroQuantityError) as exc_info:
        Product("Товар", "Описание", 100.0, 0)
    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)


def test_product_positive_quantity_creates():
    """Тест создания товара с положительным количеством."""
    product = Product("Товар", "Описание", 100.0, 5)
    assert product.quantity == 5


def test_category_middle_price_with_products():
    """Тест среднего ценника категории с товарами."""
    product1 = Product("Товар1", "Описание", 100.0, 2)
    product2 = Product("Товар2", "Описание", 200.0, 3)
    category = Category("Тест", "Описание", [product1, product2])
    assert category.middle_price() == 150.0  # (100 + 200) / 2 = 150


def test_category_middle_price_empty():
    """Тест среднего ценника пустой категории."""
    category = Category("Пустая", "Описание")
    assert category.middle_price() == 0


def test_category_add_product_zero_quantity():
    """Тест добавления товара с нулевым количеством в категорию."""
    category = Category("Тест", "Описание")
    product = Product("Товар", "Описание", 100.0, 5)
    product.quantity = 0  # Меняем количество на 0

    with pytest.raises(ZeroQuantityError):
        category.add_product(product)


def test_zeroquantityerror_is_valueerror():
    """Тест, что ZeroQuantityError является ValueError."""
    assert issubclass(ZeroQuantityError, ValueError)


def test_main_scenario_works():
    """Тест сценария из main.py работает."""
    # Проверяем исключение при нулевом количестве
    with pytest.raises(ValueError) as exc_info:  # Ловим как ValueError
        Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)

    # Создаем нормальные товары
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создаем категорию и проверяем среднюю цену
    category = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])
    expected_avg = (180000.0 + 210000.0 + 31000.0) / 3
    assert category.middle_price() == expected_avg

    # Проверяем пустую категорию
    empty_category = Category("Пустая категория", "Категория без продуктов", [])
    assert empty_category.middle_price() == 0


def test_existing_functionality_still_works():
    """Тест, что существующая функциональность по-прежнему работает."""
    product = Product("Тест", "Описание", 100.0, 5)
    assert product.name == "Тест"
    assert product.price == 100.0

    # Проверяем сложение
    product2 = Product("Тест2", "Описание", 200.0, 3)
    result = product + product2
    assert result == (100.0 * 5) + (200.0 * 3)

    # Проверяем категорию
    category = Category("Тест", "Описание", [product, product2])
    assert len(category) == 2
    assert str(category) == "Тест, количество продуктов: 8 шт."
