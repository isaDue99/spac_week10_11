# module to handle database connection

import mysql.connector as sql
import database_config as db_conf


def get_adapter() -> "AdapterI":
    """Return the appropriate database adapter class (subclass of AdapterI interface) according to database_config.SYSTEM setting"""
    if db_conf.SYSTEM == "MySQL":
        return MySQLAdapter()
    else:
        raise Exception(f"database_configuration.SYSTEM setting (=\"{db_conf.SYSTEM}\") not recognized")


class AdapterI:
    """An \"interface\" for the operations that specific implementations of database connections should support. Functionality is implemented by subclasses"""
    
    def find(self, query):
        """Returns one item matching SQL query"""
        pass

    def find_all(self, query):
        """Returns all items matching SQL query"""
        pass

    def execute(self, query):
        """Executes (and commits) the SQL statement"""
        pass


class Database:
    """
    Represents a connection to a database. 
    Automatically adapts to the database system in use, as indicated by the database_config.SYSTEM setting.
    """

    def __init__(self):
        self.client = get_adapter()

    def find_params(self, table, params: dict):
        """
        Find rows in table that match the given dict (params), of the shape {"column name": (value to search for)}.
        """
        # construct sql statement from params

        # start the query
        query = f"SELECT * FROM {table} WHERE "

        # first key we add doesn't need AND-clause
        pop_key, pop_value = params.popitem()
        query += f"{pop_key}={pop_value} "
        
        # then add any subsequent params as AND-clauses
        for key, value in params.items():
            if type(value) is str:
                query += f"AND {key}=\"{value}\" "
            else:
                query += f"AND {key}={value} "
        query += ";"

        print(query)

        # pass this query to adapter
        return self.client.find_all(query)
    
    def find_param(self, table, key, value):
        """
        Find a product in (table) with value (value) in column (key)
        """
        # SQL needs string values to be enclosed in quotes, but numeric values must be free
        if type(value) is str:
            query = f"SELECT * FROM {table} WHERE {key}=\"{value}\";"
        else:
            query = f"SELECT * FROM {table} WHERE {key}={value};"
        return self.client.find_all(query)
    
    def find_id(self, table, id):
        """
        Find a product in (table) given (id)
        """
        query = f"SELECT * FROM {table} WHERE ID={id};"
        return self.client.find(query)
    
    def get_table(self, table):
        """
        Get absolutely every row in a table. Equivalent to "SELECT * FROM (table)"
        """
        query = f"SELECT * FROM {table};"

        return self.client.find_all(query)
    
    def test_add(self):
        query = f"INSERT INTO Products (ID, Type, Name, Price, Currency, Stock) VALUES (1002, 'Test3', 'Test Product 3', 69, 'SEK', 17)"

        return self.client.execute(query)
    
    # TODO the rest etc..


class MySQLAdapter(AdapterI):
    """Connection to a MySQL database"""

    def __init__(self):
        self.conn = sql.connect(user=db_conf.USERNAME, password=db_conf.PASSWORD)
        self._init_db_and_tables(db_conf.DATABASE_NAME)
    

    # messy section, initially copied from https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
    ###

    def _init_db_and_tables(self, database):
        """
        Connects to database named (database), creating a new one if it doesnt exist. 
        Then creates tables on this database if they dont already exist
        """        
        
        cur = self.conn.cursor()
        self._set_db(cur, database)
        self._create_tables(cur, db_conf.TABLES)
        cur.close()


    def _set_db(self, cursor, DB_NAME):
        """Sets which database to use for connection. If database doesnt exist already then it is created"""
        try:
            cursor.execute(f"USE {DB_NAME}")
        except sql.Error as err:
            if err.errno == sql.errorcode.ER_BAD_DB_ERROR:
                self._create_db(cursor, DB_NAME)
                self.conn.database = DB_NAME
            else:
                print(err)
                exit(1)

    def _create_db(self, cursor, DB_NAME):
        """Attempts to create a new database"""
        try:
            cursor.execute(
                f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        except sql.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    def _create_tables(self, cursor, TABLES):
        """Creates tables in database if they dont already exist"""
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print(f"Creating table {table_name}: ", end='')
                cursor.execute(table_description)
            except sql.Error as err:
                if err.errno == sql.errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

    ###
    # back to regularly scheduled functions


    def find(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        return result
    
    def find_all(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result

    def execute(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()