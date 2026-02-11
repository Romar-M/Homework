import pytest
from src.models import Product, Category, ZeroQuantityError, Smartphone, LawnGrass, BaseProduct, LogCreationMixin
from unittest.mock import patch
import io
import sys


class TestProductClass:
    """Расширенные тесты для класса Product."""

    def test_product_str_method(self):
        """Тест строкового представления Product."""
        product = Product("Тест", "Описание", 100.0, 5)
        assert str(product) == "Тест, 100.0 руб. Остаток: 5 шт."

    def test_product_repr_method(self):
        """Тест метода __repr__ для Product."""
        product = Product("Тест", "Описание", 100.0, 5)
        assert repr(product) == "Product('Тест', 'Описание', 100.0, 5)"

    def test_product_price_setter_negative(self, capsys):
        """Тест сеттера цены с отрицательным значением."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = -50.0

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

    def test_product_price_setter_zero(self, capsys):
        """Тест сеттера цены с нулевым значением."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = 0.0

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0

    def test_product_price_setter_positive(self):
        """Тест сеттера цены с положительным значением."""
        product = Product("Тест", "Описание", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    def test_product_new_product_classmethod(self):
        """Тест класс-метода new_product."""
        data = {
            "name": "Новый товар",
            "description": "Описание",
            "price": 200.0,
            "quantity": 3
        }
        product = Product.new_product(data)
        assert isinstance(product, Product)
        assert product.name == "Новый товар"
        assert product.price == 200.0
        assert product.quantity == 3

    def test_product_new_product_zero_quantity(self):
        """Тест new_product с нулевым количеством."""
        data = {
            "name": "Товар",
            "description": "Описание",
            "price": 100.0,
            "quantity": 0
        }
        with pytest.raises(ZeroQuantityError):
            Product.new_product(data)

    def test_product_addition_same_type(self):
        """Тест сложения товаров одного типа."""
        p1 = Product("Товар1", "Описание", 100.0, 2)
        p2 = Product("Товар2", "Описание", 200.0, 3)
        result = p1 + p2
        assert result == (100.0 * 2) + (200.0 * 3)

    def test_product_addition_different_types(self):
        """Тест сложения товаров разных типов."""
        p1 = Product("Товар1", "Описание", 100.0, 2)
        p2 = Smartphone("Смартфон", "Описание", 200.0, 3, 95.5, "Модель", 128, "Черный")
        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            p1 + p2


class TestSmartphoneClass:
    """Тесты для класса Smartphone."""

    def test_smartphone_creation(self):
        """Тест создания смартфона."""
        smartphone = Smartphone(
            "iPhone", "Смартфон", 100000.0, 10,
            95.5, "15 Pro", 256, "Черный"
        )
        assert smartphone.name == "iPhone"
        assert smartphone.price == 100000.0
        assert smartphone.quantity == 10
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Черный"

    def test_smartphone_str_method(self):
        """Тест строкового представления Smartphone."""
        smartphone = Smartphone("Тест", "Описание", 100.0, 5, 95.5, "Модель", 128, "Черный")
        # Наследует __str__ от Product
        assert str(smartphone) == "Тест, 100.0 руб. Остаток: 5 шт."

    def test_smartphone_repr_method(self):
        """Тест метода __repr__ для Smartphone."""
        smartphone = Smartphone("Тест", "Описание", 100.0, 5, 95.5, "Модель", 128, "Черный")
        expected = "Smartphone('Тест', 'Описание', 100.0, 5, 95.5, 'Модель', 128, 'Черный')"
        assert repr(smartphone) == expected

    def test_smartphone_zero_quantity(self):
        """Тест создания смартфона с нулевым количеством."""
        with pytest.raises(ZeroQuantityError):
            Smartphone("Тест", "Описание", 100.0, 0, 95.5, "Модель", 128, "Черный")


class TestLawnGrassClass:
    """Тесты для класса LawnGrass."""

    def test_lawngrass_creation(self):
        """Тест создания газонной травы."""
        grass = LawnGrass(
            "Трава", "Газонная", 500.0, 20,
            "Россия", "7 дней", "Зеленый"
        )
        assert grass.name == "Трава"
        assert grass.price == 500.0
        assert grass.quantity == 20
        assert grass.country == "Россия"
        assert grass.germination_period == "7 дней"
        assert grass.color == "Зеленый"

    def test_lawngrass_str_method(self):
        """Тест строкового представления LawnGrass."""
        grass = LawnGrass("Тест", "Описание", 100.0, 5, "Россия", "7 дней", "Зеленый")
        # Наследует __str__ от Product
        assert str(grass) == "Тест, 100.0 руб. Остаток: 5 шт."

    def test_lawngrass_repr_method(self):
        """Тест метода __repr__ для LawnGrass."""
        grass = LawnGrass("Тест", "Описание", 100.0, 5, "Россия", "7 дней", "Зеленый")
        expected = "LawnGrass('Тест', 'Описание', 100.0, 5, 'Россия', '7 дней', 'Зеленый')"
        assert repr(grass) == expected

    def test_lawngrass_zero_quantity(self):
        """Тест создания газонной травы с нулевым количеством."""
        with pytest.raises(ZeroQuantityError):
            LawnGrass("Тест", "Описание", 100.0, 0, "Россия", "7 дней", "Зеленый")


class TestCategoryClass:
    """Расширенные тесты для класса Category."""

    def setup_method(self):
        """Сбрасываем счетчики перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_len_method(self):
        """Тест метода __len__ для Category."""
        product = Product("Товар", "Описание", 100.0, 5)
        category = Category("Тест", "Описание", [product])
        assert len(category) == 1

    def test_category_get_products_list(self):
        """Тест метода get_products_list."""
        product = Product("Товар", "Описание", 100.0, 5)
        category = Category("Тест", "Описание", [product])
        products_list = category.get_products_list()
        assert len(products_list) == 1
        assert products_list[0] == product

    def test_category_products_getter(self):
        """Тест геттера products."""
        product1 = Product("Товар1", "Описание", 100.0, 5)
        product2 = Product("Товар2", "Описание", 200.0, 3)
        category = Category("Тест", "Описание", [product1, product2])

        products_str = category.products
        assert "Товар1, 100.0 руб. Остаток: 5 шт." in products_str
        assert "Товар2, 200.0 руб. Остаток: 3 шт." in products_str

    def test_category_add_product_success(self, capsys):
        """Тест успешного добавления товара."""
        category = Category("Тест", "Описание")
        product = Product("Товар", "Описание", 100.0, 5)

        category.add_product(product)

        captured = capsys.readouterr()
        assert "Товар 'Товар' успешно добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert len(category) == 1

    def test_category_add_product_zero_quantity(self, capsys):
        """Тест добавления товара с нулевым количеством."""
        category = Category("Тест", "Описание")
        product = Product("Товар", "Описание", 100.0, 5)
        product.quantity = 0

        with pytest.raises(ZeroQuantityError):
            category.add_product(product)

        captured = capsys.readouterr()
        assert "с нулевым количеством не может быть добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_category_add_non_product(self, capsys):
        """Тест добавления не-продукта."""
        category = Category("Тест", "Описание")

        with pytest.raises(TypeError):
            category.add_product("не продукт")

        captured = capsys.readouterr()
        assert "Можно добавлять только продукты или их наследники" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_category_middle_price_single_product(self):
        """Тест среднего ценника с одним товаром."""
        product = Product("Товар", "Описание", 150.0, 5)
        category = Category("Тест", "Описание", [product])
        assert category.middle_price() == 150.0

    def test_category_middle_price_multiple_products(self):
        """Тест среднего ценника с несколькими товарами."""
        p1 = Product("Т1", "Описание", 100.0, 2)
        p2 = Product("Т2", "Описание", 200.0, 3)
        p3 = Product("Т3", "Описание", 300.0, 1)
        category = Category("Тест", "Описание", [p1, p2, p3])
        assert category.middle_price() == 200.0  # (100+200+300)/3

    def test_category_middle_price_empty(self):
        """Тест среднего ценника пустой категории."""
        category = Category("Тест", "Описание")
        assert category.middle_price() == 0

    def test_category_counters(self):
        """Тест счетчиков категорий и продуктов."""
        assert Category.category_count == 0
        assert Category.product_count == 0

        category1 = Category("Кат1", "Описание")
        assert Category.category_count == 1

        product = Product("Товар", "Описание", 100.0, 5)
        category1.add_product(product)
        assert Category.product_count == 1

        category2 = Category("Кат2", "Описание")
        assert Category.category_count == 2


class TestAbstractClassesAndMixin:
    """Тесты для абстрактных классов и миксинов."""

    def test_baseproduct_is_abstract(self):
        """Тест, что BaseProduct абстрактный."""
        assert hasattr(BaseProduct, '__abstractmethods__')

        # Нельзя создать экземпляр
        with pytest.raises(TypeError):
            BaseProduct("Тест", "Описание", 100.0, 5)

    def test_product_implements_baseproduct(self):
        """Тест, что Product реализует BaseProduct."""
        product = Product("Тест", "Описание", 100.0, 5)
        assert isinstance(product, BaseProduct)

    def test_logcreationmixin_prints(self, capsys):
        """Тест, что миксин выводит информацию при создании."""
        product = Product("Тест", "Описание", 100.0, 5)
        captured = capsys.readouterr()
        assert "Product('Тест', 'Описание', 100.0, 5)" in captured.out


class TestIntegration:
    """Интеграционные тесты."""

    def test_full_scenario(self):
        """Полный сценарий работы магазина."""
        # Создаем товары
        smartphone = Smartphone(
            "iPhone 15", "Смартфон", 100000.0, 5,
            95.5, "15 Pro", 256, "Черный"
        )
        grass = LawnGrass(
            "Трава", "Газонная", 500.0, 20,
            "Россия", "7 дней", "Зеленый"
        )
        product = Product("Обычный товар", "Описание", 1000.0, 10)

        # Создаем категории
        electronics = Category("Электроника", "Техника", [smartphone])
        garden = Category("Сад", "Для сада", [grass])
        other = Category("Другое", "Прочее", [product])

        # Проверяем средние цены
        assert electronics.middle_price() == 100000.0
        assert garden.middle_price() == 500.0
        assert other.middle_price() == 1000.0

        # Добавляем товары в категории
        new_product = Product("Новый товар", "Описание", 2000.0, 3)
        electronics.add_product(new_product)

        # Проверяем обновленную среднюю цену
        assert electronics.middle_price() == 51000.0  # (100000 + 2000) / 2

        # Проверяем сложение товаров одного типа
        product1 = Product("Т1", "Описание", 100.0, 2)
        product2 = Product("Т2", "Описание", 200.0, 3)
        assert product1 + product2 == 800.0  # 100*2 + 200*3

        # Проверяем обработку ошибок
        with pytest.raises(ZeroQuantityError):
            Product("Бракованный", "Описание", 100.0, 0)


def test_coverage_edges():
    """Тесты для достижения полного покрытия."""

    # Тест на наследование
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)
    assert issubclass(ZeroQuantityError, ValueError)

    # Тест свойств Product
    product = Product("Тест", "Описание", 100.0, 5)
    assert product.name == "Тест"
    assert product.description == "Описание"

    # Тест Category.__str__
    category = Category("Тест", "Описание")
    assert str(category) == "Тест, количество продуктов: 0 шт."

    product = Product("Товар", "Описание", 100.0, 3)
    category.add_product(product)
    assert str(category) == "Тест, количество продуктов: 3 шт."
