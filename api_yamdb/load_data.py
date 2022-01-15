import os
import csv
import sqlite3

# con = sqlite3.connect(os.path.abspath(os.path.join(os.path.dirname(__file__), 'db.sqlite3')))

# cursorObj = con.cursor()
# table_name = 'reviews_category'
# cursorObj.execute(f'Delete from {table_name}')
# con.commit()

# cursor.executescript("""
#  insert into Artist values (Null, 'A Aagrh!');
#  insert into Artist values (Null, 'A Aagrh-2!');
# """)


csv_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'static/data/'))
db_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'db.sqlite3'))


class CsvToSqlLite(object):
    def __init__(self, csv_folder, db_path):
        self.csv_folder = csv_folder
        self.db_path = db_path

    def read_csv(self, file_name, required_fields={}):
        file_path = os.path.join(self.csv_folder, file_name)
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            data_list = [r for r in data]
            print(data_list)
            if required_fields:
                print('prep')
                for k, v in required_fields.items():
                    data_list[0].append(k)
                    for value_list in data_list[1:]:
                        value_list.append(v)
            print(data_list)
        return data_list

    def generate_sql_query_with_insert_commands(self, table_name, data):
        column_names = ', '.join(data[0])
        insert_template = f'INSERT INTO {table_name} ({column_names}) VALUES ({{}});'
        insert_lines = [insert_template.format(', '.join(f"'{value}'" for value in row)) for row in data[1:]]
        return '\n'.join(insert_lines)

    def delete_table_in_db(self, table_name):
        con = sqlite3.connect(self.db_path)
        cursorObj = con.cursor()
        cursorObj.execute(f'Delete from {table_name}')
        con.commit()
        con.close()

    def insert_in_db(self, sql_query):
        con = sqlite3.connect(self.db_path)
        cursorObj = con.cursor()
        cursorObj.executescript(sql_query)
        con.commit()
        con.close()

    def read_csv_and_insert_in_db(self, file_name, table_name, required_fields={}):
        data = self.read_csv(file_name, required_fields)
        query = self.generate_sql_query_with_insert_commands(table_name, data)
        print(query)
        self.delete_table_in_db(table_name)
        self.insert_in_db(query)


my_instance = CsvToSqlLite(csv_path, db_path)

#my_instance.read_csv_and_insert_in_db('category.csv', 'reviews_category')
# не понятно как быть с FK
#my_instance.read_csv_and_insert_in_db('comments.csv', 'reviews_comment')
# my_instance.read_csv_and_insert_in_db('genre_title.csv', 'reviews_titlegenre')
# my_instance.read_csv_and_insert_in_db('genre.csv', 'reviews_genre')
#my_instance.read_csv_and_insert_in_db('review.csv', 'reviews_review')
#my_instance.read_csv_and_insert_in_db('titles.csv', 'reviews_title')
my_instance.read_csv_and_insert_in_db('users.csv', 'users_user', {'password': 'qqq', 'is_superuser': 'True', 'is_staff': 'True'})



# data = self.read_csv('category.csv', 'reviews_category')

# data_list = my_instance.read_csv('category.csv')
# sql = my_instance.generate_sql_with_insert_commands('reviews_category', data_list)
# print(data_list)
# print(sql)




# genre = read_csv(csv_path, 'genre.csv')
# review = read_csv(csv_path, 'review.csv')
# titles = read_csv(csv_path, 'titles.csv')
# users = read_csv(csv_path, 'users.csv')

# print(categories)
# print(comments)
# print(genre_title)
# print(genre)
# print(review)
# print(titles)
# print(users)
