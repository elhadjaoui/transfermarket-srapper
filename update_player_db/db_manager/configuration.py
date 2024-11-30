from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    try:
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1] # param[0] is the key, param[1] is the value
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return db
    except Exception as e:
        print(e)
        return None