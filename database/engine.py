import configparser
import os
from sqlalchemy import create_engine

home_path = os.path.expanduser("~")

""""
config.ini example

[mysql]
username=your_username
password=your_password
host=your_host
port=your_port
database=your_database
[ai_api]
key = my_key
url= ai_flask_url
"""

config_path = os.path.join(home_path, 'config.ini')


# Read the configuration file
config = configparser.ConfigParser()
config.read(config_path)

# Get the MySQL connection details from the configuration file
username = config.get('mysql', 'username')
password = config.get('mysql', 'password')
host = config.get('mysql', 'host')
port = config.get('mysql', 'port')
database = config.get('mysql', 'database')

# Create the database engine
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}',echo=False)

