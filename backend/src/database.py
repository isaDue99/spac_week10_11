# module to handle database connection

import os
import mysql.connector as sql


class AdapterI:
    """An \"interface\" for the operations that specific implementations of database connections should support. Functionality is implemented by subclasses"""

    def find(self, selector):
        """Returns 1 item matching SQL selector"""
        pass

    def find_all(self, selector):
        """Returns all items matching SQL selector"""
        pass

    def create(self, query):
        """Creates a new row using SQL query"""
        pass

    def update(self, query):
        """Updates items using SQL query"""
        pass

    def delete(self, selector):
        """Deletes items matching SQL selector"""
        pass


class Database:
    """Represents a connection to a database"""

    def __init__(self, adapter: AdapterI):
        """
        Constructor for Database objects. 
        
        (adapter) provides the specific implementations of common database operations, depending on what type of database is in use. 
        For example, if the database is MySQL, then (adapter) should be an instance of the MySQLAdapter class.
        """
        self.client = adapter()

    def find(self, params):
        """
        Find a product in database given (params). TODO
        """
        # construct sql statement from params
        query = params

        # pass this query to adapter
        return self.client.find(query)
    
    def get_table(self, table):
        """
        Get absolutely every row in a table. Equivalent to "SELECT * FROM (table)"
        """
        query = f"SELECT * FROM {table}"

        return self.client.find_all(query)
    
    # TODO the rest etc..


class MySQLAdapter(AdapterI):
    """Connection to a MySQL database"""

    def __init__(self):
        user = "root"
        password = os.environ.get("MYSQL_ROOT_PASSWORD")
        database = "fullstack_db"
        self.conn = sql.connect(user=user, password=password)
        self._init_db_and_tables(database)
    

    # messy section, initially copied from https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
    ###

    def _init_db_and_tables(self, database):
        """
        Connects to database named (database), creating a new one if it doesnt exist. 
        Then creates tables on this database if they dont already exist
        """

        TABLES = {}
        TABLES['Products'] = (
            "CREATE TABLE `Products` ("
            "   `name` varchar(40) NOT NULL,"
            "   `price` float NOT NULL,"
            "   `stock` int NOT NULL,"
            "   `weight` int NOT NULL,"
            "   `calories` int NOT NULL,"
            "   `protein` int NOT NULL,"
            "   `fat` int NOT NULL,"
            "   `carbs` int NOT NULL,"
            "   `sugars` int NOT NULL,"
            "   `fiber` int NOT NULL,"
            "   `vitamins` int NOT NULL,"
            "   PRIMARY KEY (`name`)"
            ") ENGINE=InnoDB")
        
        cur = self.conn.cursor()
        self._set_db(cur, database)
        self._create_tables(cur, TABLES)
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

    def find(self, selector):
        cur = self.conn.cursor()
        cur.execute(selector)
        result = cur.fetchone()
        cur.close()
        return result
    
    def find_all(self, selector):
        cur = self.conn.cursor()
        cur.execute(selector)
        result = cur.fetchall()
        cur.close()
        return result

    def create(self, query):
        self._alter_db(self, query)

    def update(self, query):
        self._alter_db(self, query)

    def delete(self, selector):
        self._alter_db(self, selector)

    def _alter_db(self, query):
        """
        Helper function to avoid code-duplication: executes database-altering (query) and commits changes.
        create(), update() and delete() are identical implementation-wise, 
        but must be kept as separate functions to comply with AdapterI contract.
        """
        cur = self.conn.cursor()
        cur.execute(query)
        # TODO add try-except before commit() is called?
        self.conn.commit()
        cur.close()


