from database.DB_connect import DBConnect
from model.driver import Driver

class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getNodi(anno1):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT DISTINCT d.driverId AS id, d.forename AS nome, d.surname AS cognome "
                 "FROM drivers d, races r, results re "
                 "WHERE d.driverId = re.driverId  AND r.raceId = re.raceId "
                 "AND re.position IS NOT NULL  AND r.year= %s "                        
                "GROUP BY d.driverId, d.forename, d.surname ")
        cursor.execute(query,(anno1,))

        for row in cursor:
            results.append(Driver(row["id"],row["nome"],row["cognome"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(anno1):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT DISTINCT re1.driverId AS id1, re2.driverId AS id2, COUNT( DISTINCT r.raceId ) AS peso  "
                 "FROM races r, results re1, results re2 "
                 "WHERE  r.raceId = re1.raceId AND r.raceId = re2.raceId "
                 "AND re1.position IS NOT NULL  AND r.year= %s "
                 "AND re1.driverId <> re2.driverId "
                 "AND re1.position < re2.position "
                 "AND re2.position IS NOT NULL "                        
                "GROUP BY re1.driverId,re2.driverId ")
        cursor.execute(query,(anno1,))

        for row in cursor:
            results.append((row["id1"],row["id2"],row["peso"]))

        cursor.close()
        conn.close()
        return results

