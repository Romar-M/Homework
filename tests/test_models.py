import pytest
import sys
from io import StringIO
from src.models import BaseProduct, LogCreationMixin, Product, Smartphone, LawnGrass, Category


def test_abstract_class_cannot_be_instantiated():
    """Тест, что абстрактный класс нельзя инстанцировать."""
    with pytest.raises(TypeError):
        BaseProduct("Тест", "Описание", 100.0, 5)


def test_product_is_subclass_of_baseproduct():
    """Тест, что Product является наследником BaseProduct."""
    assert issubclass(Product, BaseProduct)


def test_mixin_prints_on_creation(capsys):
    """Тест, что миксин выводит информацию при создании объекта."""
    # Создаем продукт
    product = Product("Тестовый продукт", "Описание", 100.0, 5)

    # Проверяем вывод
    captured = capsys.readouterr()
    assert "Product('Тестовый продукт', 'Описание', 100.0, 5)" in captured.out


def test_smartphone_prints_on_creation(capsys):
    """Тест, что Smartphone выводит информацию при создании."""
    smartphone = Smartphone(
        name="Тестовый смартфон",
        description="Описание",
        price=200.0,
        quantity=3,
        efficiency=95.5,
        model="Модель X",
        memory=256,
        color="Черный"
    )

    captured = capsys.readouterr()
    assert "Smartphone('Тестовый смартфон', 'Описание', 200.0, 3, 95.5, 'Модель X', 256, 'Черный')" in captured.out


def test_mixin_in_inheritance_chain():
    """Тест, что миксин находится в цепочке наследования Product."""
    mro = Product.__mro__
    assert LogCreationMixin in mro
    assert BaseProduct in mro


def test_existing_functionality_still_works():
    """Тест, что существующая функциональность по-прежнему работает."""
    product = Product("Тест", "Описание", 100.0, 5)
    assert product.name == "Тест"
    assert product.price == 100.0
    assert str(product) == "Тест, 100.0 руб. Остаток: 5 шт."

    product2 = Product("Тест2", "Описание2", 200.0, 3)
    result = product + product2
    assert result == (100.0 * 5) + (200.0 * 3)
