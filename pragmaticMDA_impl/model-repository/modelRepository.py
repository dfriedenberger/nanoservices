import json
import yaml

from mysql.connector import connect, Error

def connect_db():

    with open("repository.yml") as f:
        config = yaml.safe_load(f)

    return connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    ) 


class Table:

    def __init__(self,tablename,parameters,types):
        self.tablename = tablename
        self.parameters = parameters
        self.types = types
    
    def create(self,obj):
        with connect_db() as connection:
            
            values = list()
            f_str = list()
            for i in range(len(self.parameters)):
                f_str.append("%s")
                value = obj[self.parameters[i]]
                if self.types[i] == "JSON":
                    value = json.dumps(value)
                values.append(value)
            
            insert_query = f"INSERT INTO {self.tablename} ({','.join(self.parameters)}) VALUES ({','.join(f_str)})"
            print(insert_query)
            with connection.cursor() as cursor:
                cursor.execute(insert_query, tuple(values))
            connection.commit()


    def read_by_id(self,id):
        with connect_db() as connection:        
            select_query = f"SELECT {','.join(self.parameters)} FROM {self.tablename} WHERE id = '{id}'"
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                row = cursor.fetchone()
                obj = {}
                for i in range(len(row)):
                    value = row[i]
                    if self.types[i] == "JSON":
                        value = json.loads(value)
                    obj[self.parameters[i]] = value

                return obj

    def update_by_id(self,obj):

        with connect_db() as connection:    

            if "id" not in obj: 
                raise ValueError(f"key 'id' not found in {obj}")
            values = list()
            assignments = list()
            for i in range(len(self.parameters)):
              
                if self.parameters[i] == "id": continue
                assignments.append(f"{self.parameters[i]} = %s")
                value = obj[self.parameters[i]]
                if self.types[i] == "JSON":
                    value = json.dumps(value)
                values.append(value)
            
            update_query = f"UPDATE {self.tablename} SET {','.join(assignments)} WHERE id = '{obj['id']}'"
            print(update_query)

            with connection.cursor() as cursor:
                cursor.execute(update_query,tuple(values))
            connection.commit()
     
    
    def delete_by_id(self,id):
         with connect_db() as connection:        
            delete_query = f"DELETE FROM {self.tablename} WHERE id = '{id}'"
            with connection.cursor() as cursor:
                cursor.execute(delete_query)
            connection.commit()




class ModelRepository:

    def __init__(self):
    
        self.table_model = Table("model",['id', 'format', 'model'],['VARCHAR(36)', 'VARCHAR(100)', 'TEXT'])
    
    def create_model(self,obj): 
        self.table_model.create(obj)

    def read_model(self,id):
        return self.table_model.read_by_id(id)

    def update_model(self,obj):
        self.table_model.update_by_id(obj)
    
    def delete_model(self,id):
        self.table_model.delete_by_id(id)
    
  