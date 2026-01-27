import pytest
from src.models import Product, Smartphone, LawnGrass, Category


class TestProductInheritance:
    """Тесты наследования классов."""

    def test_smartphone_is_subclass_of_product(self):
        """Тест, что Smartphone является наследником Product."""
        assert issubclass(Smartphone, Product)

    def test_lawngrass_is_subclass_of_product(self):
        """Тест, что LawnGrass является наследником Product."""
        assert issubclass(LawnGrass, Product)

    def test_smartphone_has_additional_attributes(self):
        """Тест, что Smartphone имеет дополнительные атрибуты."""
        smartphone = Smartphone(
            name="Тест",
            description="Описание",
            price=100.0,
            quantity=5,
            efficiency=95.5,
            model="Модель",
            memory=256,
            color="Черный"
        )

        assert hasattr(smartphone, 'efficiency')
        assert hasattr(smartphone, 'model')
        assert hasattr(smartphone, 'memory')
        assert hasattr(smartphone, 'color')
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "Модель"
        assert smartphone.memory == 256
        assert smartphone.color == "Черный"

    def test_lawngrass_has_additional_attributes(self):
        """Тест, что LawnGrass имеет дополнительные атрибуты."""
        grass = LawnGrass(
            name="Трава",
            description="Описание",
            price=500.0,
            quantity=10,
            country="Россия",
            germination_period="7 дней",
            color="Зеленый"
        )

        assert hasattr(grass, 'country')
        assert hasattr(grass, 'germination_period')
        assert hasattr(grass, 'color')
        assert grass.country == "Россия"
        assert grass.germination_period == "7 дней"
        assert grass.color == "Зеленый"

    def test_smartphone_inherits_product_methods(self):
        """Тест, что Smartphone наследует методы Product."""
        smartphone = Smartphone("Тест", "Описание", 100.0, 5, 95.5, "Модель", 256, "Черный")

        # Проверяем унаследованные методы
        assert smartphone.price == 100.0
        smartphone.price = 150.0
        assert smartphone.price == 150.0
        assert str(smartphone) == "Тест, 150.0 руб. Остаток: 5 шт."


class TestProductAdditionRestrictions:
    """Тесты ограничений на сложение товаров."""

    def test_add_same_product_types(self):
        """Тест сложения товаров одного типа (Product)."""
        product1 = Product("Товар1", "Описание", 100.0, 10)
        product2 = Product("Товар2", "Описание", 200.0, 5)

        result = product1 + product2
        expected = (100.0 * 10) + (200.0 * 5)
        assert result == expected

    def test_add_same_smartphone_types(self):
        """Тест сложения смартфонов."""
        smartphone1 = Smartphone("Смарт1", "Описание", 100.0, 2, 95.5, "Модель1", 128, "Черный")
        smartphone2 = Smartphone("Смарт2", "Описание", 200.0, 3, 98.2, "Модель2", 256, "Белый")

        result = smartphone1 + smartphone2
        expected = (100.0 * 2) + (200.0 * 3)
        assert result == expected

    def test_add_same_lawngrass_types(self):
        """Тест сложения газонной травы."""
        grass1 = LawnGrass("Трава1", "Описание", 500.0, 4, "Россия", "7 дней", "Зеленый")
        grass2 = LawnGrass("Трава2", "Описание", 600.0, 6, "США", "5 дней", "Темно-зеленый")

        result = grass1 + grass2
        expected = (500.0 * 4) + (600.0 * 6)
        assert result == expected

    def test_add_different_product_types_raises_error(self):
        """Тест, что сложение разных типов товаров вызывает ошибку."""
        smartphone = Smartphone("Смарт", "Описание", 100.0, 2, 95.5, "Модель", 128, "Черный")
        grass = LawnGrass("Трава", "Описание", 500.0, 4, "Россия", "7 дней", "Зеленый")

        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            smartphone + grass

    def test_add_product_with_smartphone_raises_error(self):
        """Тест, что сложение Product и Smartphone вызывает ошибку."""
        product = Product("Товар", "Описание", 100.0, 5)
        smartphone = Smartphone("Смарт", "Описание", 200.0, 3, 95.5, "Модель", 128, "Черный")

        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            product + smartphone

    def test_type_function_used_in_add(self):
        """Тест, что в методе __add__ используется функция type()."""
        # Создаем два объекта одного типа
        smartphone1 = Smartphone("Смарт1", "Описание", 100.0, 2, 95.5, "Модель1", 128, "Черный")
        smartphone2 = Smartphone("Смарт2", "Описание", 200.0, 3, 98.2, "Модель2", 256, "Белый")

        # Сложение должно пройти успешно
        result = smartphone1 + smartphone2
        assert result == (100.0 * 2) + (200.0 * 3)

        # Проверяем, что типы действительно одинаковые
        assert type(smartphone1) == type(smartphone2)


class TestCategoryAddProductRestrictions:
    """Тесты ограничений на добавление товаров в категорию."""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_add_product_to_category(self):
        """Тест добавления обычного товара в категорию."""
        category = Category("Тест", "Описание")
        product = Product("Товар", "Описание", 100.0, 5)

        initial_count = Category.product_count
        category.add_product(product)

        assert len(category) == 1
        assert Category.product_count == initial_count + 1

    def test_add_smartphone_to_category(self):
        """Тест добавления смартфона в категорию."""
        category = Category("Тест", "Описание")
        smartphone = Smartphone("Смарт", "Описание", 100.0, 2, 95.5, "Модель", 128, "Черный")

        category.add_product(smartphone)
        assert len(category) == 1

    def test_add_lawngrass_to_category(self):
        """Тест добавления газонной травы в категорию."""
        category = Category("Тест", "Описание")
        grass = LawnGrass("Трава", "Описание", 500.0, 4, "Россия", "7 дней", "Зеленый")

        category.add_product(grass)
        assert len(category) == 1

    def test_add_non_product_raises_error(self):
        """Тест, что добавление не-продукта вызывает ошибку."""
        category = Category("Тест", "Описание")

        with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследники"):
            category.add_product("Не продукт")

    def test_add_integer_raises_error(self):
        """Тест, что добавление целого числа вызывает ошибку."""
        category = Category("Тест", "Описание")

        with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследники"):
            category.add_product(123)

    def test_add_list_raises_error(self):
        """Тест, что добавление списка вызывает ошибку."""
        category = Category("Тест", "Описание")

        with pytest.raises(TypeError, match="Можно добавлять только продукты или их наследники"):
            category.add_product([1, 2, 3])

    def test_isinstance_used_in_add_product(self):
        """Тест, что в методе add_product используется isinstance()."""
        category = Category("Тест", "Описание")

        # isinstance должен возвращать True для Product и его наследников
        product = Product("Товар", "Описание", 100.0, 5)
        smartphone = Smartphone("Смарт", "Описание", 100.0, 2, 95.5, "Модель", 128, "Черный")
        grass = LawnGrass("Трава", "Описание", 500.0, 4, "Россия", "7 дней", "Зеленый")

        assert isinstance(product, Product)
        assert isinstance(smartphone, Product)
        assert isinstance(grass, Product)

        # Все они должны быть успешно добавлены
        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        assert len(category) == 3


class TestExistingFunctionality:
    """Тесты на сохранение старой функциональности."""

    def test_product_str_method_still_works(self):
        """Тест, что метод __str__ у Product по-прежнему работает."""
        product = Product("Телефон", "Смартфон", 50000.0, 10)
        assert str(product) == "Телефон, 50000.0 руб. Остаток: 10 шт."

    def test_category_str_method_still_works(self):
        """Тест, что метод __str__ у Category по-прежнему работает."""
        product = Product("Товар", "Описание", 100.0, 3)
        category = Category("Тест", "Описание", [product])
        assert str(category) == "Тест, количество продуктов: 3 шт."

    def test_price_validation_still_works(self):
        """Тест, что валидация цены по-прежнему работает."""
        product = Product("Тест", "Описание", 100.0, 5)

        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        product.price = -50

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        assert "Цена не должна быть нулевая или отрицательная" in output
        assert product.price == 100.0

    def test_new_product_classmethod_still_works(self):
        """Тест, что класс-метод new_product по-прежнему работает."""
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


def test_main_example_works():
    """Тест, что пример из main.py работает без ошибок."""
    # Имитируем выполнение кода из main.py
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                             "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    # Проверяем сложение товаров одного класса
    smartphone_sum = smartphone1 + smartphone2
    expected_smartphone_sum = (180000.0 * 5) + (210000.0 * 8)
    assert smartphone_sum == expected_smartphone_sum

    grass_sum = grass1 + grass2
    expected_grass_sum = (500.0 * 20) + (450.0 * 15)
    assert grass_sum == expected_grass_sum

    # Проверяем ошибку при сложении разных классов
    try:
        invalid_sum = smartphone1 + grass1
        assert False, "Должна была возникнуть ошибка TypeError"
    except TypeError:
        pass

    # Проверяем добавление товаров в категорию
    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    assert len(category_smartphones) == 2

    # Проверяем ошибку при добавлении не-продукта
    try:
        category_smartphones.add_product("Not a product")
        assert False, "Должна была возникнуть ошибка TypeError"
    except TypeError:
        pass
