import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view._txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDAnno(self):
        for a in self._model.getAnni():
            self._view._ddAnno.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        # 1. pulisco l'output
        self._view._txt_result.controls.clear()

        # 2. leggo i due anni (il dropdown restituisce una stringa, oppure None)
        if self._view._ddAnno.value is None :
            self._errore("Selezionare entrambi gli anni!")
            return
        anno1 = int(self._view._ddAnno.value)

        # 4. creo il grafo
        self._model.buildGraph(anno1)

        # 5. stampo nodi e archi
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()

        # il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a. i 3 archi di peso maggiore
        self._view._txt_result.controls.append(ft.Text("Top 3 archi di peso maggiore:"))
        for i, (u, v, peso) in enumerate(self._model.getTop3(), start=1):
            self._view._txt_result.controls.append(
                ft.Text(f"{i}. {u} -> {v} (arrivato davanti {peso} volte)"))

        # b. pilota migliore
        pilota, valore = self._model.getPilotaMigliore()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Pilota migliore: {pilota} (uscenti - entranti = {valore})"))

        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleDreamTeam(self, e):
        self._view._txt_result.controls.clear()

        # 1. il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # 2. leggo K
        try:
            k = int(self._view._txtInK.value)
        except (ValueError, TypeError):
            self._errore("K deve essere un numero intero!")
            return
        if k < 1 or k > 5:
            self._errore("K deve essere compreso tra 1 e 5!")
            return
        if k > self._model.getNumNodi():
            self._errore(f"Il grafo ha solo {self._model.getNumNodi()} piloti!")
            return

        # 3. ricorsione
        team, valore = self._model.getDreamTeam(k)
        if len(team) == 0:
            self._errore("Nessun team trovato!")
            return

        # 4. stampa: piloti in ordine alfabetico + vittorie esterne
        self._view._txt_result.controls.append(ft.Text(f"Dream Team di {k} piloti:"))
        for p in sorted(team, key=lambda x: str(x)):
            self._view._txt_result.controls.append(ft.Text(f"- {p}"))
        self._view._txt_result.controls.append(ft.Text(f"Vittorie esterne: {valore}"))
        self._view.update_page()

