import configparser


class ConfigLoader:
    def __init__(self, config_path):
        """
        Initializes a new instance of the ConfigLoader class.

        Args:
            config_path (str): The path to the configuration file.

        Initializes the `config` attribute of the class with a ConfigParser object,
        which reads the configuration file specified by `config_path`.

        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_db_config(self):
        """
        Retrieves the database configuration from the config file.

        :return: A dictionary containing the database configuration with the following keys:
                 - 'username': The username for the database.
                 - 'password': The password for the database.
                 - 'host': The host for the database.
                 - 'port': The port for the database.
                 - 'database': The name of the database.
        :rtype: dict
        """
        return {
            'username': self.config.get('copypatrol_db', 'username'),
            'password': self.config.get('copypatrol_db', 'password'),
            'host': self.config.get('copypatrol_db', 'host'),
            'port': int(self.config.get('copypatrol_db', 'port')),
            'database': self.config.get('copypatrol_db', 'database')
        }
