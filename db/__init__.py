import psycopg2 as ps
from configparser import ConfigParser


def load_config(filename="./config/database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return config


CONFIG = load_config()
    

def connect(config=CONFIG):
    """Connect to the PostgreSQL database server"""
    try:
        # connecting to the PostgreSQL server
        with ps.connect(**config) as conn:
            print("Connected to the PostgreSQL server.")
            return conn, conn.cursor()
    except (ps.DatabaseError, Exception) as error:
        print(error)