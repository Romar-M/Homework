import pytest
from src.models import BaseProduct, LogCreationMixin, Product, Smartphone, LawnGrass, Category


def test_abstract_class_cannot_be_instantiated():
    """Тест, что абстрактный класс нельзя инстанцировать."""
    with pytest.raises(TypeError):
        BaseProduct("Тест", "Описание", 100.0, 5)


def test_product_is_subclass_of_baseproduct():
    """Тест, что Product является наследником BaseProduct."""
    assert issubclass(Product, BaseProduct)


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


def test_smartphone_creation():
    """Тест создания смартфона."""
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

    assert smartphone.name == "Тестовый смартфон"
    assert smartphone.price == 200.0
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "Модель X"
    assert smartphone.memory == 256
    assert smartphone.color == "Черный"


def test_lawngrass_creation():
    """Тест создания газонной травы."""
    grass = LawnGrass(
        name="Тестовая трава",
        description="Описание",
        price=500.0,
        quantity=10,
        country="Россия",
        germination_period="7 дней",
        color="Зеленый"
    )

    assert grass.name == "Тестовая трава"
    assert grass.price == 500.0
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_product_implements_abstract_methods():
    """Тест, что Product реализует абстрактные методы."""
    product = Product("Тест", "Описание", 100.0, 5)

    # Проверяем, что абстрактные методы реализованы
    assert hasattr(product, 'name')
    assert product.name == "Тест"

    assert hasattr(product, 'price')
    assert product.price == 100.0


def test_mixin_prints_on_creation(capsys):
    """Тест, что миксин выводит информацию при создании объекта."""
    product = Product("Тестовый продукт", "Описание", 100.0, 5)

    captured = capsys.readouterr()
    assert "Product('Тестовый продукт', 'Описание', 100.0, 5)" in captured.out


def test_category_add_product():
    """Тест добавления продукта в категорию."""
    category = Category("Тест", "Описание")
    product = Product("Товар", "Описание", 100.0, 5)

    category.add_product(product)
    assert len(category) == 1


def test_category_add_non_product_raises_error():
    """Тест, что добавление не-продукта вызывает ошибку."""
    category = Category("Тест", "Описание")

    with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследники"):
        category.add_product("Не продукт")


def test_addition_with_same_type():
    """Тест сложения товаров одного типа."""
    product1 = Product("Товар1", "Описание", 100.0, 2)
    product2 = Product("Товар2", "Описание", 200.0, 3)

    result = product1 + product2
    assert result == (100.0 * 2) + (200.0 * 3)


def test_addition_with_different_types_raises_error():
    """Тест, что сложение разных типов вызывает ошибку."""
    smartphone = Smartphone("Смарт", "Описание", 100.0, 2, 95.5, "Модель", 128, "Черный")
    grass = LawnGrass("Трава", "Описание", 500.0, 4, "Россия", "7 дней", "Зеленый")

    with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
        smartphone + grass


def test_category_str_method():
    """Тест строкового представления категории."""
    product1 = Product("Товар1", "Описание", 100.0, 3)
    product2 = Product("Товар2", "Описание", 200.0, 2)

    category = Category("Тест", "Описание", [product1, product2])

    assert str(category) == "Тест, количество продуктов: 5 шт."


def test_product_str_method():
    """Тест строкового представления продукта."""
    product = Product("Телефон", "Смартфон", 50000.0, 10)
    assert str(product) == "Телефон, 50000.0 руб. Остаток: 10 шт."


def test_price_validation():
    """Тест валидации цены."""
    product = Product("Тест", "Описание", 100.0, 5)

    # Проверяем отрицательную цену
    product.price = -50
    assert product.price == 100.0  # Цена не должна измениться

    # Проверяем нулевую цену
    product.price = 0
    assert product.price == 100.0  # Цена не должна измениться

    # Проверяем положительную цену
    product.price = 150.0
    assert product.price == 150.0


def test_new_product_classmethod():
    """Тест класс-метода new_product."""
    product_data = {
        "name": "Новый товар",
        "description": "Описание",
        "price": 200.0,
        "quantity": 3
    }
    product = Product.new_product(product_data)

    assert product.name == "Новый товар"
    assert product.price == 200.0
    assert product.quantity == 3


def test_category_counters():
    """Тест счетчиков категорий и продуктов."""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    # Создаем категорию с продуктами
    product1 = Product("Товар1", "Описание", 100.0, 3)
    product2 = Product("Товар2", "Описание", 200.0, 2)

    category = Category("Тест", "Описание", [product1, product2])

    assert Category.category_count == 1
    assert Category.product_count == 2

    # Добавляем еще один продукт
    product3 = Product("Товар3", "Описание", 300.0, 5)
    category.add_product(product3)

    assert Category.product_count == 3


def test_products_getter():
    """Тест геттера для списка товаров."""
    product1 = Product("Товар1", "Описание1", 100.0, 5)
    product2 = Product("Товар2", "Описание2", 200.0, 3)

    category = Category("Тест", "Описание", [product1, product2])

    products_str = category.products
    assert "Товар1, 100.0 руб. Остаток: 5 шт." in products_str
    assert "Товар2, 200.0 руб. Остаток: 3 шт." in products_str
