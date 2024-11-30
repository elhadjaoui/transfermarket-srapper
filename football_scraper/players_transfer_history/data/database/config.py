from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1] # param[0] is the key, param[1] is the value
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


config()
# Path: add_data_to_pgsql.py
# Compare this snippet from add_data_to_pgsql.py:
# import psycopg2 as pg
#
# # Connect to an existing database
# conn = pg.connect("dbname=postgres user=postgres")
#
# # Open a cursor to perform database operations
# cur = conn.cursor()
#
# # Execute a command: this creates a new table
# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
#
# # Pass data to fill a query placeholders and let Psycopg perform
# # the correct conversion (no more SQL injections!)
# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))