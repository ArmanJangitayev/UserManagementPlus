from django.db import connection


class SQLDBManager:
    def connect_to_db(self):
        # Метод для установки соединения с базой данных
        return connection

    def execute_query(self, query, params=None):
        con = self.connect_to_db()
        # Метод для выполнения SQL-запроса
        with con.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()  # Получение результатов запроса, если они есть
        return result
