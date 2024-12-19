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
        """Executes (and commits) the SQL statement. Returns last row ID if relevant on INSERT and UPDATE operations"""
        pass


class Database:
    """
    Represents a connection to a database. 
    Automatically adapts to the database system in use, as indicated by the database_config.SYSTEM setting.
    """

    def __init__(self):
        self.client = get_adapter()

    def find_by_params(self, table, params: dict):
        """
        Find rows in (table) that match the given dict (params), of the shape {"column name": (value to search for)}.
        """

        # construct sql statement from params
        query = f"SELECT * FROM {table} WHERE "
        query += self._construct_sql_list(params, " AND ", mode="=")
        query += ";"

        # pass this query to adapter
        return self.client.find_all(query)          

    def get_table(self, table):
        """
        Get absolutely every row in (table). Basically "SELECT * FROM (table)"
        """

        query = f"SELECT * FROM {table};"
        return self.client.find_all(query)
    
    def create(self, table, body: dict):
        """
        Adds new row to (table), using column-value pairs in (body)
        """

        cols, vals = self._construct_sql_list(body, ", ", mode="separate")
        query = f"INSERT INTO {table} ({cols}) VALUES ({vals});"
        return self.client.execute(query)
    
    def update(self, table, args: dict, body: dict):
        """
        Updates rows in (table) that match column-value pairs in (args), using column-value pairs in (body)
        """

        query = f"UPDATE {table} SET "
        query += self._construct_sql_list(body, ", ", mode="=")
        query += f" WHERE "
        query += self._construct_sql_list(args, " AND ", mode="=")
        query += ";"
        return self.client.execute(query)
    
    def delete(self, table, args: dict | None):
        """
        Deletes rows from (table) that match column-value pairs in (args). 
        If args is None, then omits the WHERE-clause and deletes all rows in (table)
        """

        query = f"DELETE FROM {table}"
        if args:
            query += " WHERE "
            query += self._construct_sql_list(args, " AND ", mode="=")
        query += ";"
        return self.client.execute(query)
    
    # helper functions
    def _construct_sql_list(self, args: dict, sep: str, mode: str):
        """
        Returns either one or two strings of the key-value pairs in (args) joined together using separator (sep).
        Depending on mode:
        "="-mode: returns one string "key1=value1(sep)key2=value2(sep)..."
        "separate"-mode: returns two strings "key1(sep)key2(sep)..." and "value1(sep)value2(sep)..."

        For SQL reasons, non-numeric values are wrapped in quotes, and numeric values aren't 
        """
        if mode == "=":
            items = []
            for key, value in args.items():
                if str.isdigit(value):
                    item = f"{key}={value}"
                else:
                    item = f"{key}=\"{value}\""
                items.append(item)
            return sep.join(items)
        elif mode == "separate":
            keys, values = ([], [])
            for key, value in args.items():
                keys.append(key)
                if str.isdigit(value):
                    values.append(value)
                else:
                    values.append(f"\"{value}\"")
            return (sep.join(keys), sep.join(values))
        else:
            print("mode not recognized")
            return ""


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
        last_id = cur.lastrowid
        self.conn.commit()
        cur.close()
        return last_id