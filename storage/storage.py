import sqlite3
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class Storage:
    """
    Класс для работы с базой данных.
    
    :param TypeValuesFromCategories: Класс, предоставляющий значения для поля Type в
    таблице Categories.
    """
    
    class TypeValues:
        """
        Класс, предоставляющий значения для поля Type в таблице Categories.
        """
        DRAGONFLY = 1  # Стрекозки
        FLY = 2  # Мушки
    
    def __init__(self, db_file='storage.db'):
        """
        Инициализирует объект и устанавливает соединение с базой данных.

        :param db_file: Имя файла базы данных.
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
        # TODO Пока по умолчанию задаются два продукта
        self.clear_tables()
        self.add_image_category_product('/assets/photo_5370574978803683622_y.jpg',
                                        self.TypeValues.DRAGONFLY,
                                        'Категория стрекоз',
                                        'Стрекоза 1',
                                        'Брошь в виде стрекозы',
                                        '5000 р.',
                                        1,
                                        0)
        self.add_image_category_product('/assets/photo_5370574978803683643_y.jpg',
                                        self.TypeValues.FLY,
                                        'Категория мушки',
                                        'Мушка 1',
                                        'Брошь в виде мушки',
                                        '5000 р.',
                                        1,
                                        0)
    
    def create_tables(self):
        """
        Создает таблицы в БД.
        """
        # Customers
        # Запись в таблице Сustomers не может быть удалена, если существует к ней связь из
        # таблицы Orders.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Login TEXT UNIQUE,
                Password TEXT,
                Admin BOOLEAN,
                FOREIGN KEY (Id) REFERENCES Orders (CustomerId) ON DELETE RESTRICT
            )
        ''')
        
        # Images
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Images (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                ImagePath TEXT UNIQUE
            )
        ''')
        
        # Categories
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                Id INTEGER PRIMARY KEY,
                Type INTEGER UNIQUE,
                Name TEXT,
                ImageId INTEGER,
                FOREIGN KEY (ImageId) REFERENCES Images (Id)
            )
        ''')
        
        # Products
        # Запись в таблице Products не может быть удалена, если существует к ней связь из
        # таблицы Orders.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Description TEXT,
                Price TEXT,
                QuantityInStock INTEGER,
                QuantityPurchased INTEGER,
                CategoryId INTEGER,
                ImageId INTEGER,
                FOREIGN KEY (CategoryId) REFERENCES Categories (Id),
                FOREIGN KEY (ImageId) REFERENCES Images (Id),
                FOREIGN KEY (Id) REFERENCES Orders (ProductId) ON DELETE RESTRICT
            )
        ''')
        
        # Orders
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Price TEXT,
                UserName TEXT,
                UserAddress TEXT,
                DeliveryType INTEGER,
                СustomerId INTEGER,
                ProductId INTEGER,
                FOREIGN KEY (СustomerId) REFERENCES Customers (Id),
                FOREIGN KEY (ProductId) REFERENCES Products (Id)
            )
        ''')
    
    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()
    
    def add_customer(self, login, password, admin=False):
        """
        Добавляет нового пользователя в таблицу Customers.
        Чтобы избежать конфликтов, login и password д.б. уникальны.

        :param login: Логин пользователя.
        :param password: Пароль пользователя.
        :param admin: Флаг администратора (по умолчанию False).
        """
        try:
            self.cursor.execute('''
                INSERT INTO Customers (Login, Password, Admin)
                VALUES (?, ?, ?)
            ''', (login, password, admin))
            self.conn.commit()
            logging.info(f"Пользователь '{login}' успешно добавлен.")
        except sqlite3.IntegrityError:
            logging.error(f"Ошибка: Пользователь с логином '{login}' уже существует.")
    
    def remove_customer(self, login):
        """
        Удаляет пользователя из таблицы Customers.

        :param login: Логин пользователя для удаления.
        """
        try:
            self.cursor.execute('''
                   DELETE FROM Customers
                   WHERE Login = ?
               ''', (login,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                logging.info(f"Пользователь '{login}' успешно удален.")
            else:
                logging.error(f"Ошибка: Пользователь с логином '{login}' не найден.")
        except Exception as e:
            logging.error(f"Ошибка при удалении пользователя '{login}': {str(e)}")
    
    def add_image(self, image_path):
        """
        Добавляет запись в таблицу Images.

        :param image_path: Путь к изображению.
        :return: Идентификатор добавленного изображения (Id) или None, если добавление не
        удалось.
        """
        try:
            self.cursor.execute('INSERT INTO Images (ImagePath) VALUES (?)', (image_path,))
            self.conn.commit()
            logging.info("Изображение успешно добавлено.")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            logging.error("Изображение с таким путем уже существует. Пожалуйста, используйте "
                          "уникальный путь.")
            return None
    
    def delete_image(self, image_id):
        """
        Удаляет запись из таблицы Images.

        :param image_id: Идентификатор изображения для удаления.
        """
        try:
            self.cursor.execute('DELETE FROM Images WHERE Id = ?', (image_id,))
            self.conn.commit()
            logging.info("Изображение успешно удалено.")
        except sqlite3.IntegrityError:
            logging.error("Ошибка удаления изображения. Проверьте, есть ли какие-либо "
                          "зависимости от этого образа.")
    
    def add_product(self, name, description, price, quantity_in_stock, quantity_purchased,
                    category_id, image_id):
        """
        Добавляет запись в таблицу Products.

        :param name: Название продукта.
        :param description: Описание продукта.
        :param price: Цена продукта.
        :param quantity_in_stock: Количество продукта в наличии.
        :param quantity_purchased: Количество продукта, проданное.
        :param category_id: Идентификатор категории продукта.
        :param image_id: Идентификатор изображения продукта.
        """
        try:
            self.cursor.execute('''
                   INSERT INTO Products (Name, Description, Price, QuantityInStock,
                   QuantityPurchased, CategoryId, ImageId)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
               ''', (
                name, description, price, quantity_in_stock, quantity_purchased, category_id,
                image_id))
            self.conn.commit()
            logging.info("Продукт успешно добавлен.")
        except sqlite3.IntegrityError:
            logging.error(
                "Ошибка добавления продукта. Проверьте уникальность данных или наличие связей.")
    
    def delete_product(self, product_id):
        """
        Удаляет запись из таблицы Products.

        :param product_id: Идентификатор продукта для удаления.
        """
        try:
            self.cursor.execute('DELETE FROM Products WHERE Id = ?', (product_id,))
            self.conn.commit()
            logging.info("Продукт успешно удален.")
        except sqlite3.IntegrityError:
            logging.error(
                "Ошибка удаления продукта. Проверьте наличие связей с другими таблицами.")
    
    def add_category(self, category_type, name, image_id):
        """
        Добавляет запись в таблицу Categories.

        :param category_type: Тип категории.
        :param name: Название категории.
        :param image_id: Идентификатор изображения категории.
        :return: Идентификатор добавленной категории (Id) или None, если добавление не
        удалось.
        """
        try:
            self.cursor.execute('INSERT INTO Categories (Type, Name, ImageId) VALUES (?, ?, ?)',
                                (category_type, name, image_id))
            self.conn.commit()
            logging.info("Категория успешно добавлена.")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            logging.error(
                "Ошибка добавления категории. Проверьте уникальность данных или наличие "
                "связей.")
            return None
    
    def delete_category(self, category_id):
        """
        Удаляет запись из таблицы Categories.

        :param category_id: Идентификатор категории для удаления.
        """
        try:
            self.cursor.execute('DELETE FROM Categories WHERE Id = ?', (category_id,))
            self.conn.commit()
            logging.info("Категория успешно удалена.")
        except sqlite3.IntegrityError:
            logging.error(
                "Ошибка удаления категории. Проверьте наличие связей с другими таблицами.")
    
    def add_order(self, price, user_name, user_address, delivery_type, customer_id, product_id):
        """
        Добавляет запись в таблицу Orders.

        :param price: Цена заказа.
        :param user_name: Имя пользователя, оформившего заказ.
        :param user_address: Адрес пользователя, оформившего заказ.
        :param delivery_type: Тип доставки.
        :param customer_id: Идентификатор заказчика.
        :param product_id: Идентификатор продукта в заказе.
        """
        try:
            self.cursor.execute('''
                INSERT INTO Orders (Price, UserName, UserAddress, DeliveryType, СustomerId, ProductId)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (price, user_name, user_address, delivery_type, customer_id, product_id))
            self.conn.commit()
            logging.info("Заказ успешно добавлен.")
        except sqlite3.IntegrityError:
            logging.error(
                "Ошибка добавления заказа. Проверьте корректность данных или наличие связей.")
    
    def delete_order(self, order_id):
        """
        Удаляет запись из таблицы Orders.

        :param order_id: Идентификатор заказа для удаления.
        """
        try:
            self.cursor.execute('DELETE FROM Orders WHERE Id = ?', (order_id,))
            self.conn.commit()
            logging.info("Заказ успешно удален.")
        except sqlite3.IntegrityError:
            logging.error(
                "Ошибка удаления заказа. Проверьте наличие связей с другими таблицами.")
    
    def clear_tables(self):
        """
        Очищает все таблицы в базе данных.
        """
        tables = ['Customers', 'Images', 'Categories', 'Products', 'Orders']
        for table in tables:
            self.cursor.execute(''' 
                            DELETE FROM {}
                        '''.format(table))
            self.conn.commit()
        logging.info("Все таблицы очищены.")
            
    def add_image_category_product(self, image_path, category_type, category_name, product_name,
                                   product_description, product_price, quantity_in_stock,
                                   quantity_purchased):
        """
        Добавляет изображение, категорию и продукт в базу данных.

        :param image_path: Путь к изображению.
        :param category_type: Тип категории.
        :param category_name: Имя категории.
        :param product_name: Имя продукта.
        :param product_description: Описание продукта.
        :param product_price: Цена продукта.
        :param quantity_in_stock: Количество на складе.
        :param quantity_purchased: Количество проданных.
        """
        image_id = self.add_image(image_path)
        if image_id is not None:
            category_id = self.add_category(category_type, category_name, image_id)
            if category_id is not None:
                self.add_product(product_name, product_description, product_price,
                                 quantity_in_stock, quantity_purchased, category_id, image_id)
            else:
                logging.error("Что-то пошло не так!")
        else:
            logging.error("Что-то пошло не так!")
