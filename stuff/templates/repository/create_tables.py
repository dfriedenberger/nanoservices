import yaml
import os

from mysql.connector import connect, Error

def read_sql_queries():
    sql_queries = []
    sql_files = [f for f in os.listdir(".") if f.startswith("create_table") and f.endswith(".sql")]
    for sql_file in sql_files:
        with open(sql_file) as f:
            for line in f:
                line = line.strip()
                if line:
                    sql_queries.append(line)
    return sql_queries



try:    
    with open("repository.yml") as f:
        config = yaml.safe_load(f)

    with connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    ) as connection:

        for create_table_query in read_sql_queries():
            with connection.cursor() as cursor:
                print(create_table_query)
                cursor.execute(create_table_query)

        connection.commit()

except Error as e:
    print(e)


