import psycopg2
from prettytable import PrettyTable


class DataBase:

    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.tables = {"terminal": ["terminal_id", "passengertraffic", "gates", "type", "runways", "cargo"],
                       "gates": ["gates_id", "throughput", "type", "terminal"],
                       "flight": ["flight_id", "passengers", "plane", "timeofarrival", "gates", "type", "runway"],
                       "runway": ["runway_id", "length", "weightallowed", "terminal"],
                       "cargodepot": ["cargo_id", "height", "volume", "numberofloaders", "terminal"]}
        try:
            self.connection = psycopg2.connect(database=self.database,
                                               user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port)
        except Exception as e:
            print("Connection failed")
            print(e.__str__())

    def perform_query(self, query):
        try:
            temp = self.connection.cursor()
            temp.execute(query)
            return temp.fetchall()
        except Exception as e:
            self.connection.cursor().close()
            self.connection.rollback()
            print(e.__str__())
            return []

    def add_entry(self, table_name):
        if table_name not in self.tables:
            print("No such table exists")
            return 0
        temp = []
        query = "INSERT INTO " + 'airport_modified.' + table_name + " ("
        query0 = " VALUES ( "
        for elem in self.tables[table_name][1:]:
            temp.append(input("Enter " + elem + " for " + table_name + "\n"))
            query = query + elem + ", "
            query0 += "%" + "(" + elem + ")" + "s, "
        query = query[:-2] + ") " + query0[:-2] + ");"
        alpha = {}
        beta = self.tables[table_name][1:].copy()
        while beta != [] or temp != []:
            alpha.update({beta.pop(0): temp.pop(0)})
        try:
            self.connection.cursor().execute(query, alpha)
            self.connection.cursor().close()
            self.connection.commit()
        except Exception as e:
            self.connection.cursor().close()
            self.connection.rollback()
            print(e.__str__())

    def delete_entry(self, table_name, search_parameter, value):
        if table_name in self.tables:
            query = "SELECT " + search_parameter + " FROM airport_modified." + table_name + " WHERE " + search_parameter + " = " \
                    + value
            try:
                temp = self.connection.cursor()
                temp.execute(query)
                a = temp.fetchall()
                if a:
                    query2 = "DELETE FROM airport_modified." + table_name + " WHERE " + search_parameter + " = " + value + ";"
                    try:
                        self.connection.cursor().execute(query2)
                        self.connection.cursor().close()
                        self.connection.commit()
                    except Exception:
                        print("Deletion failed, you have connected entries in other tables")
                        self.connection.rollback()
                else:
                    print("No such entry found")
            except Exception as e:
                self.connection.rollback()
                print(e.__str__())
        else:
            print("No such table exists")

    def update_entry(self, table_name, search_parameter, value):
        if table_name in self.tables:
            query = "SELECT " + search_parameter + " FROM airport_modified." + table_name + " WHERE " \
                                                                                "" + search_parameter + " = " + value
            try:
                temp = self.connection.cursor()
                temp.execute(query)
                a = temp.fetchall()
                if a:
                    query = "UPDATE airport_modified." + table_name + " SET "
                    for elem in self.tables[table_name][1:]:
                        loc_elem = str(input("Enter " + elem + " for " + table_name + "\n"))
                        if elem in ["type", "plane", "timeofarrival"]:
                            loc_elem = "'" + loc_elem + "'"
                        query += elem + " = " + loc_elem + ", "
                    query = query[:-2] + " WHERE " + search_parameter + " = " + value
                    try:
                        self.connection.cursor().execute(query)
                        self.connection.cursor().close()
                        self.connection.commit()
                    except Exception as e:
                        self.connection.rollback()
                        print("Could not update entry")
                        print(e.__str__())
                else:
                    print("No such entry found")
            except Exception as e:
                print(e.__str__())
                self.connection.rollback()
            print("Record successfully updated")
        else:
            print("No such table exists")

    def show_table(self, table_name):
        if table_name in self.tables:
            x = PrettyTable()
            x.field_names = self.tables[table_name]
            temp = []
            try:
                cur = self.connection.cursor()
                cur.execute("SELECT * FROM airport_modified." + table_name)
                temp = cur.fetchall()
                cur.close()
            except Exception as e:
                self.connection.rollback()
                print("Fetching failed")
                print(e)
            if temp:
                for elem in temp:
                    x.add_row(list(elem))
            print(x)
        else:
            print("No such table found")
