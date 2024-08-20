import pymysql


class Database:
    def __init__(self, config):
        """
        Initializes a new instance of the Database class.

        Parameters:
            config (dict): A dictionary containing the configuration parameters for the database connection.
                - host (str): The host of the database.
                - port (int): The port number of the database.
                - username (str): The username for the database.
                - password (str): The password for the database.
                - database (str): The name of the database.

        Returns:
            None
        """
        self.conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['username'],
            password=config['password'],
            database=config['database']
        )

    def execute_query(self, query, params=None):
        """
        Executes a SQL query on the database and returns the first row of the result.

        Parameters:
            query (str): The SQL query to execute.
            params (Optional[tuple]): The parameters to be used in the query. Defaults to None.

        Returns:
            Optional[tuple]: The first row of the result, or None if the result is empty.
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def close(self):
        """
        Closes the connection to the database.

        This method closes the connection to the database by calling the `close()` method of the `self.conn` object.

        Parameters:
            None

        Returns:
            None
        """
        self.conn.close()
