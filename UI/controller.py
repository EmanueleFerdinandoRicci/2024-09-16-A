import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_ddshape(self):
        shapes = self._model.getAllShapes()
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handle_graph(self, e):
        minlat,maxlat = self._model.getLat()
        minlng,maxlng = self._model.getLng()
        if self._view.txt_latitude.value == "" and self._view.txt_longitude.value == "":
            self._view.txt_result1.controls.append(ft.Text("Inserisci valori numerici Lat e Lng."))
            self._view.update_page()
            return
        try:
            lat = float(self._view.txt_latitude.value)
            lng = float(self._view.txt_longitude.value)
        except ValueError:
            self._view.txt_result1.controls.append(ft.Text("Inserisci valori numerici Lat e Lng."))
            self._view.update_page()
            return
        if lat > maxlat or lat < minlat:
            self._view.txt_result1.controls.append(ft.Text(f"Inserisci valori di Lat tra {minlat} e {maxlat}"))
            self._view.update_page()
            return
        if lng > maxlng or lng < minlng:
            self._view.txt_result1.controls.append(ft.Text(f"Inserisci valori di Lng tra {minlng} e {maxlng}"))
            self._view.update_page()
            return

        self._model.creaGrafo(self._view.ddshape.value,lat,lng)
        n, m = self._model.getGraphDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(
            ft.Text(f"Grafo correttamente creato! Ha {n} nodi e {m} archi")
        )
        edges = self._model.getEdgeGrandi()
        count = 0
        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 archi con peso maggiore:")
        )
        for e in edges:
            if count < 5:
                self._view.txt_result1.controls.append(
                    ft.Text(f"{e[0]} --> {e[1]}: {e[2]["weight"]}")
                )
                count += 1
        num, largest, details = self._model.getCompConnessa()
        count2 = 0
        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 nodi con grado maggiore:")
        )
        for e in details:
            if count2 < 5:
                self._view.txt_result1.controls.append(
                    ft.Text(f"{e[0]} --> {e[1]}")
                )
                count2 += 1
        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_path(self, e):
        path, score = self._model.getPath()

        self._view.txt_result2.controls.clear()
        if not path:
            self._view.txt_result2.controls.append(ft.Text("Nessun percorso valido trovato."))
            self._view.update_page()
            return

        # Stampa del punteggio totale ottimo
        self._view.txt_result2.controls.append(
            ft.Text(f"Punteggio totale ottimo: {score:.5f}")
        )
        self._view.txt_result2.controls.append(ft.Text("Stati attraversati nel cammino:"))

        # Stampa della lista degli stati con le rispettive densità
        for s in path:
            densita = self._model.get_density(s)
            self._view.txt_result2.controls.append(
                ft.Text(f"- {s.Name} (Densità: {densita:.2f} ab/km²)")
            )

        self._view.update_page()