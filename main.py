import Database
from time import sleep
from prettytable import PrettyTable

if __name__ == '__main__':
    conn = True
    db = None
    try:
        db = Database.DataBase(database="LabDB",
                               user="postgres",
                               password="Sevenseventy770",
                               host="localhost",
                               port="5432")
    except Exception as e:
        print(e.__str__())
        conn = False

    if db is not None:
        print("Welcome!")
        while conn:
            print("====================\n"
                  "1: Add Record\n"
                  "2: Update Record\n"
                  "3: Delete Record\n"
                  "4: Show Table\n"
                  "5: Show all Tables\n"
                  "6: Cross-table queries\n"
                  "7: Exit")
            decision = input()
            print("Enter:")
            if decision == "1":
                db.add_entry(input("Table name:\n").lower())
            elif decision == "2":
                db.update_entry(input("Table name:\n".lower()), input("Search parameter:\n"), input("Value:\n"))
            elif decision == "3":
                db.delete_entry(input("Table name:\n".lower()), input("Search parameter:\n"), input("Value:\n"))
            elif decision == "4":
                db.show_table(input("Table name:\n".lower()))
            elif decision == "5":
                for table in db.tables:
                    print(table.capitalize())
                    db.show_table(table)
            elif decision == "6":
                trg = True
                while trg:
                    print("====================\n"
                          "1: Number of flights of given type\n"
                          "2: Gates info for each terminal\n"
                          "3: Gates throughput left\n"
                          "4: Flights Timetable\n"
                          "5: \n"
                          "6: Exit")
                    loc_decision = input()
                    if loc_decision == "1":
                        temp = db.perform_query("""SELECT type as "Type", 
                                            COUNT(flight_id) as "Number of flights"
                                            FROM airport_modified.flight
                                            GROUP BY type""")
                        if temp:
                            x = PrettyTable(["Type", "Number of Flights"])
                            for elem in temp:
                                x.add_row(list(elem))
                            print(x)
                        else:
                            print("Query returned empty list")
                    elif loc_decision == "2":
                        temp = db.perform_query("""SELECT terminal as "Terminal", ROUND(avg(throughput), 2) as "Average Throughput",
                                                  (SELECT COUNT(gates_id) from airport_modified.gates where gates.type='cargo') 
                                                   as "Number of Cargo gates"
                                                   FROM airport_modified.gates
                                                   GROUP BY terminal ORDER BY terminal asc""")
                        if temp:
                            x = PrettyTable(["Terminal", "Average Throughput", "Number of Cargo Gates"])
                            for elem in temp:
                                x.add_row(list(elem))
                            print(x)
                        else:
                            print("Query returned empty list")
                    elif loc_decision == "3":
                        temp = db.perform_query("""SELECT gates as Gates, (gates.throughput - SUM(flight.passengers)) as "Passengers throughput left"
                                                   FROM airport_modified.flight
                                                   INNER JOIN airport_modified.Gates ON flight.gates=Gates.gates_id
                                                   GROUP BY gates.throughput, flight.gates ORDER BY flight.gates asc""")
                        if temp:
                            x = PrettyTable(["Gates", "Passengers throughput left"])
                            for elem in temp:
                                x.add_row(list(elem))
                            print(x)
                        else:
                            print("Query returned empty list")
                    elif loc_decision == "4":
                        runways = list(db.perform_query("""SELECT runway_id 
                                                                              FROM airport_modified.runway"""))
                        query = """SELECT timeofarrival, """
                        if runways:
                            for elem in runways:
                                query += """CASE runway WHEN '""" + str(list(elem).pop()) + """' THEN flight_id ELSE 0 
                                END AS "Runway """ + str(list(elem).pop()) + '",\n'
                        query = query[:-2] + """ FROM airport_modified.flight
                                                GROUP BY timeofarrival, runway, flight_id ORDER BY timeofarrival ASC"""
                        temp = db.perform_query(query)
                        if temp:
                            x = PrettyTable(["Time of Arrival"] +
                                            ["Runway " + str(list(elem).pop()) for elem in runways])
                            for elem in temp:
                                x.add_row(list(elem))
                            print(x)
                        else:
                            print("Query returned empty list")
                    elif loc_decision == "5":
                        temp = db.perform_query("""""")
                        if temp:
                            x = PrettyTable(["", ""])
                            for elem in temp:
                                x.add_row(list(elem))
                            print(x)
                        else:
                            print("Query returned empty list")
                    elif loc_decision == "6":
                        trg = False
            elif decision == "7":
                conn = False
            sleep(2)
