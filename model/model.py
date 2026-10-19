import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()  # orientato: A -> B = A davanti a B
        self._idMap = {}  # driverId -> oggetto Driver

        # punto 2 (Dream Team)
        self._nodi = []  # lista dei piloti, per usare gli indici
        self._K = 0  # quanti piloti nel team
        self._teamBest = []  # miglior team trovato
        self._valBest = -1


    def getAnni(self):
        return DAO.getAllYears()

    def buildGraph(self, anno):
        self._grafo.clear()
        self._idMap = {}
        nodi = DAO.getNodi(anno)
        self._idMap = {d.driverId: d for d in nodi}
        self._grafo.add_nodes_from(nodi)
        for id1, id2, peso in DAO.getEdges(anno):
            if id1 in self._idMap and id2 in self._idMap:
                self._grafo.add_edge(self._idMap[id1], self._idMap[id2], weight=peso)

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getTop3(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            archi.append((u, v, dati["weight"]))
        archi.sort(key=lambda x: (-x[2], str(x[0]), str(x[1])))
        return archi[:3]
    def getPilotaMigliore(self):
        best = None
        valBest = None
        for p in self._grafo.nodes:
            val = self._grafo.out_degree(p, weight="weight") - self._grafo.in_degree(p, weight="weight")
            if valBest is None or val > valBest:
                best = p
                valBest = val
        return best, valBest

    # ==================== PUNTO 2 ====================

    def getDreamTeam(self, K):
        self._nodi = list(self._grafo.nodes)   # lista: serve per usare gli indici
        self._K = K
        self._teamBest = []
        self._valBest = -1
        self._ricorsione([], 0)
        return self._teamBest, self._valBest

    def _vittorieEsterne(self, team):
        squadra = set(team)
        tot = 0
        for u, v, dati in self._grafo.edges(data=True):
            if u in squadra and v not in squadra:     # arco che ESCE dal team
                tot += dati["weight"]
        return tot

    def _ricorsione(self, parziale, start):
        # caso terminale: il team ha K piloti
        if len(parziale) == self._K:
            val = self._vittorieEsterne(parziale)
            if val > self._valBest:
                self._valBest = val
                self._teamBest = list(parziale)
            return

        # aggiungo un pilota, solo tra quelli da start in poi
        for i in range(start, len(self._nodi)):
            parziale.append(self._nodi[i])
            self._ricorsione(parziale, i + 1)
            parziale.pop()                    # backtracking