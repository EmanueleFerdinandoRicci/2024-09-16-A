import copy

from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapS = {}
        self._states = []
        self._best_path = []
        self._best_score = 0.0

    def getLat(self):
        lats = DAO.getLat()
        min = float(lats[0])
        max = float(lats[-1])
        return min,max

    def getLng(self):
        lngs = DAO.getLng()
        min = float(lngs[0])
        max = float(lngs[-1])
        return min,max

    def getAllShapes(self):
        return DAO.getAllShapes()

    def creaGrafo(self,shape,lat,lng):
        self._graph.clear()
        self._states = DAO.getAllNodes(shape,lat,lng)
        for s in self._states:
            self._idMapS[s.id] = s
        self._graph.add_nodes_from(self._states)

        allEdges = DAO.getAllEdges(shape,lat,lng, self._idMapS)
        pesi = DAO.getPesi(shape,lat,lng, self._idMapS)
        dizionario_pesi = {}
        for p in pesi:
            dizionario_pesi[p.s] = p.time
        for e in allEdges:
            peso_totale = 0
            if e.s1 in dizionario_pesi:
                peso_totale += dizionario_pesi[e.s1]
            if e.s2 in dizionario_pesi:
                peso_totale += dizionario_pesi[e.s2]
            self._graph.add_edge(e.s1,e.s2, weight=peso_totale)

        #pesi = DAO.getPesi(shape,lat,lng,self._idMapS)
        #dizionario_pesi = {}
        #for p in pesi:
        #    dizionario_pesi[p.s] = p.time
        #for s in self._states:
        #    for y in self._states:
        #        # Controlla se y.id è nella lista pulita E se s.id < y.id
        #        if y.id in s.Neighbors and s.id < y.id:
        #            peso_totale = 0
        #            if s in dizionario_pesi:
        #                peso_totale += dizionario_pesi[s]
        #            if y in dizionario_pesi:
        #                peso_totale += dizionario_pesi[y]
        #            self._graph.add_edge(s,y,weight=peso_totale)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getEdgeGrandi(self):
        edgeGrandi = list(self._graph.edges(data=True))
        edgeGrandi.sort(key=lambda e: e[2]["weight"], reverse=True)
        return edgeGrandi

    def getCompConnessa(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)

        subgraph = self._graph.subgraph(largest).copy()
        orderedNodes = sorted(subgraph.nodes(),key=lambda n:self._graph.degree(n),reverse=True)

        details = [(n,self._graph.degree(n)) for n in orderedNodes]
        return len(components), largest, details

    def get_density(self, state):
        if state.Area == 0:
            return 0
        return state.Population / state.Area

    def getPath(self):
        self._best_path = []
        self._best_score = 0.0
        for n in self._graph.nodes:
            self._ricorsione(n, [n], 0.0, 0.0)
        return self._best_path, self._best_score

    def _ricorsione(self, nodo_corr, cammino_corr, peso_corr, dist_corr):
        if len(cammino_corr) > 1:
            score = peso_corr / dist_corr
            if score > self._best_score:
                self._best_score = score
                self._best_path = copy.deepcopy(list(cammino_corr))

        for vicino in self._graph.neighbors(nodo_corr):
            if self.get_density(vicino) > self.get_density(nodo_corr):
                arco_peso = self._graph[nodo_corr][vicino]['weight']
                arco_dist = float(nodo_corr.distance_HV(vicino))

                cammino_corr.append(vicino)
                self._ricorsione(vicino, cammino_corr, peso_corr + float(arco_peso), dist_corr + arco_dist)
                cammino_corr.pop()