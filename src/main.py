from models import Product, Category

if __name__ == "__main__":
    # Создаем продукты
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создаем категорию с начальными продуктами
    # Теперь продукты передаются в конструктор и автоматически добавляются через add_product()
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]  # Продукты будут добавлены через add_product()
    )

    print("Список товаров в категории:")
    print(category1.products)  # Используем геттер

    print("\n" + "=" * 50 + "\n")

    # Добавляем новый товар через метод add_product()
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)

    print("Список товаров после добавления:")
    print(category1.products)

    print(f"\nОбщее количество товаров во всех категориях: {Category.product_count}")

    print("\n" + "=" * 50 + "\n")

    # Используем класс-метод для создания продукта
    new_product = Product.new_product({
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
    })

    print(f"Создан через new_product: {new_product.name}")
    print(f"Описание: {new_product.description}")
    print(f"Цена: {new_product.price}")
    print(f"Количество: {new_product.quantity}")

    print("\n" + "=" * 50 + "\n")

    # Тестируем сеттер цены
    print("Тестирование сеттера цены:")
    print(f"Текущая цена: {new_product.price}")

    new_product.price = 800  # Устанавливаем новую цену
    print(f"Цена после установки 800: {new_product.price}")

    # Пытаемся установить невалидные цены
    print("\nПопытка установить отрицательную цену:")
    new_product.price = -100  # Выведет сообщение об ошибке
    print(f"Цена после попытки установить -100: {new_product.price}")

    print("\nПопытка установить нулевую цену:")
    new_product.price = 0  # Выведет сообщение об ошибке
    print(f"Цена после попытки установить 0: {new_product.price}")

    print("\n" + "=" * 50 + "\n")

    # Дополнительная информация
    print("Дополнительная информация:")
    print(f"Количество товаров в категории: {len(category1)}")
    print(f"Количество категорий всего: {Category.category_count}")
    print(f"Количество товаров всего: {Category.product_count}")
