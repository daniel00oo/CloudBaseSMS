import sqlite3


class StorageSqlite3(object):
    def __init__(self, name='database'):
        self.name = name
        self.db = sqlite3.connect(name + ".db")
        self.c = self.db.cursor()

    def __exit__(self, type, val, tb):
        self.db.close()

    def createDatabase(self,  params):

        if isinstance(params, dict):
            parameters = ""

            for key in params:
                parameters += key + ' ' + params[key] + ", "

            parameters = parameters[:-2]
            tmp = """CREATE TABLE {} (
                    {}
                )""".format(self.name, parameters)
        elif isinstance(params, str):
            tmp = """CREATE TABLE {} (
                    {}
                )""".format(self.name, params)

        try:
            self.c.execute(tmp)
            self.db.commit()
        except sqlite3.OperationalError:
            return(1)

        return(0)

    def insert(self, info):
        # input: info - a list of elements to be inserted
        #    ex.: ["Mary", "Johnes", 20] if the model
        #           is (first_name, last_name, salary)
        #    ex.: ["Mary", "Johnes", NULL]
        #    any type SQL type is allowed

        query = "INSERT INTO {name} {keys} VALUES({values});".format(
            name=self.name,
            keys='(' + ', '.join(info.keys()) + ')',
            values="'" + "', '".join(info.values()) + "'")

        self.c.execute(query)
        self.db.commit()

    def select(self, info):
        query = "SELECT {info} FROM {name}".format(info=info, name=self.name)
        self.c.execute(query, {'name': self.name, 'info': info})
        self.db.commit()

    def query(self, query):
        self.c.execute(query)
        self.db.commit()
