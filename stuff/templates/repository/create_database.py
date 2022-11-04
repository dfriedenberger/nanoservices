import yaml
from mysql.connector import connect, Error




try:    
    with open("repository.yml") as f:
        user = yaml.safe_load(f)

    with open("database.yml") as f:
        config = yaml.safe_load(f)

    with connect(
        host=config['host'],
        user=config['user'],
        password=config['password']
    ) as connection:

        # CREATE USER 'username'@'%' IDENTIFIED BY 'password';
        # GRANT ALL PRIVILEGES ON database.* TO 'username'@'%' WITH GRANT OPTION;
        # FLUSH PRIVILEGES;

        create_user_query = f"CREATE USER '{user['user']}'@'%' IDENTIFIED BY '{user['password']}'"
        create_database = f"CREATE DATABASE {user['database']}"
        grant_query = f"GRANT ALL PRIVILEGES ON {user['database']}.* TO '{user['user']}'@'%' WITH GRANT OPTION"
        flush_query = f"FLUSH PRIVILEGES"

        with connection.cursor() as cursor:
            print(create_user_query)
            cursor.execute(create_user_query)
            print(create_database)
            cursor.execute(create_database)
            print(grant_query)
            cursor.execute(grant_query)
            print(flush_query)
            cursor.execute(flush_query)

        connection.commit()

except Error as e:
    print(e)


