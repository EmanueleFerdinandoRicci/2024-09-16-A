from database.DB_connect import DBConnect
from model.edge import Edge
from model.peso import Peso
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getLat():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.Lat) as lat
                        from state s 
                        order by s.Lat asc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["lat"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getLng():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.Lng) as lng
                        from state s 
                        order by s.Lng asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["lng"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.shape) as shape
                        from sighting s 
                        where s.shape != "" and s.shape != 'unknown' 
                        order by s.shape desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(shape,lat,lng):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.id) as id, s.Name as name, s.Capital as cap, s.Lat as lat, s.Lng as lng, s.Area as area, s.Population as pop, s.Neighbors as nei
                        from state s, sighting si
                        where s.id = si.state and si.shape = %s and s.Lat > %s and s.Lng > %s"""
            cursor.execute(query, (shape,lat,lng,))

            for row in cursor:
                # LA MAGIA È QUI: se non è NULL, splitta per SPAZIO!
                neigh = row["nei"].split() if row["nei"] is not None else []
                result.append(State(row["id"],row["name"],row["cap"],row["lat"],row["lng"],row["area"],row["pop"],neigh))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getPesi(shape, lat, lng, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as id, sum(si.duration) as time
                        from state s, sighting si
                        where s.id = si.state and si.shape = %s and s.Lat > %s and s.Lng > %s
                        group by s.id 
                        order by s.id"""
            cursor.execute(query, (shape, lat, lng,))

            for row in cursor:
                result.append(Peso(idMap[row["id"]],row["time"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(shape, lat, lng, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1, s2.id as id2
                        from (
                            select distinct s.id, s.Neighbors as nei
                            from state s, sighting si
                            where s.id = si.state and si.shape = %s and s.Lat > %s and s.Lng > %s
                        ) s1,
                        (
                            select distinct s.id
                            from state s, sighting si
                            where s.id = si.state and si.shape = %s and s.Lat > %s and s.Lng > %s
                        ) s2
                        where s1.nei LIKE CONCAT('%', s2.id, '%') 
                        and s1.id < s2.id"""
            cursor.execute(query, (shape, lat, lng,shape, lat, lng,))

            for row in cursor:
                result.append(Edge(idMap[row["id1"]],idMap[row["id2"]]))
            cursor.close()
            cnx.close()
        return result