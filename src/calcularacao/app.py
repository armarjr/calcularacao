import toga
from toga.style import Pack
from toga.style.pack import COLUMN

# Tupla de dicionários com tipos de ração e suas fórmulas
tupla_racoes = (
    {
        "tipo_de_racao": "galinha crescimento",
        "formula_de_racao": "milho 58%, soja 31%, trigo 6%, nucleo 5%, calcário 0%",
    },
    {
        "tipo_de_racao": "galinha engorda",
        "formula_de_racao": "milho 59.5%, soja 17.5%, trigo 18%, nucleo 500%, calcário 0%",
    },
    {
        "tipo_de_racao": "galinha postura",
        "formula_de_racao": "milho 54.46%, soja 24.21%, trigo 18.15%, nucleo 1.82%, calcário 1.36%",
    },
    {
        "tipo_de_racao": "codorna crescimento",
        "formula_de_racao": "milho 58%, soja 31%, trigo 6%, nucleo 5%, calcário 0%",
    },
    {
        "tipo_de_racao": "codorna postura",
        "formula_de_racao": "milho 61%, soja 25%, trigo 0%, nucleo 7%, calcário 7%",
    },
)


class RacaoApp(toga.App):

    def startup(self):
        # Definir a janela principal
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Criar um contêiner principal
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Criação do widget Selection
        self.selection = toga.Selection(
            items=[racao["tipo_de_racao"] for racao in tupla_racoes],
            style=Pack(padding=5),
        )

        # Botão para calcular a ração
        button = toga.Button(
            "Calcular Pesos", on_press=self.calcular_pesos, style=Pack(padding=5)
        )

        # TextInput para o peso total da ração
        self.total_weight_input = toga.TextInput(
            style=Pack(padding=5), placeholder="Peso Total da Ração (kg)"
        )

        # Labels e TextInputs para os componentes da fórmula
        self.milho_input = toga.TextInput(
            style=Pack(padding=5), placeholder="Peso Milho (kg)"
        )
        self.soja_input = toga.TextInput(
            style=Pack(padding=5), placeholder="Peso Soja (kg)"
        )
        self.trigo_input = toga.TextInput(
            style=Pack(padding=5), placeholder="Peso Trigo (kg)"
        )
        self.nucleo_input = toga.TextInput(
            style=Pack(padding=5), placeholder="Peso Núcleo (kg)"
        )
        self.calcario_input = toga.TextInput(
            style=Pack(padding=5), placeholder="Peso Calcário (kg)"
        )

        # Adicionar os widgets ao contêiner
        main_box.add(self.selection)
        main_box.add(self.total_weight_input)
        main_box.add(self.milho_input)
        main_box.add(self.soja_input)
        main_box.add(self.trigo_input)
        main_box.add(self.nucleo_input)
        main_box.add(self.calcario_input)
        main_box.add(button)

        # Definir o contêiner principal como o conteúdo da janela
        self.main_window.content = main_box
        self.main_window.show()

    def calcular_pesos(self, widget):
        tipo_desejado = self.selection.value
        formula = None
        for racao in tupla_racoes:
            if racao["tipo_de_racao"] == tipo_desejado:
                formula = racao["formula_de_racao"]
                break

        if not formula:
            self.main_window.info_dialog(
                "Erro", f"Tipo de ração '{tipo_desejado}' não encontrado."
            )
            return

        components = self.parse_formula(formula)

        milho_percentage = float(components["milho"].replace("%", ""))
        soja_percentage = float(components["soja"].replace("%", ""))
        trigo_percentage = float(components["trigo"].replace("%", ""))
        nucleo_percentage = float(components["nucleo"].replace("%", ""))
        calcario_percentage = float(components["calcário"].replace("%", ""))

        total_weight = self.get_weight(self.total_weight_input.value)

        if total_weight > 0:
            # Calculate the weight of each component based on the total weight and percentage
            milho_weight = (milho_percentage * total_weight) / 100
            soja_weight = (soja_percentage * total_weight) / 100
            trigo_weight = (trigo_percentage * total_weight) / 100
            nucleo_weight = (nucleo_percentage * total_weight) / 100
            calcario_weight = (calcario_percentage * total_weight) / 100

            result_text = (
                f"Peso Total da Ração: {total_weight:.2f} kg\n"
                f"Milho: {milho_weight:.2f} kg\n"
                f"Soja: {soja_weight:.2f} kg\n"
                f"Trigo: {trigo_weight:.2f} kg\n"
                f"Núcleo: {nucleo_weight:.2f} kg\n"
                f"Calcário: {calcario_weight:.2f} kg"
            )

            self.main_window.info_dialog("Resultado", result_text)
        else:
            # Calculate the total weight and other components based on a single component input
            milho_weight = self.get_weight(self.milho_input.value)
            soja_weight = self.get_weight(self.soja_input.value)
            trigo_weight = self.get_weight(self.trigo_input.value)
            nucleo_weight = self.get_weight(self.nucleo_input.value)
            calcario_weight = self.get_weight(self.calcario_input.value)

            # Check if more than one component is filled
            filled_components = [
                weight
                for weight in [
                    milho_weight,
                    soja_weight,
                    trigo_weight,
                    nucleo_weight,
                    calcario_weight,
                ]
                if weight > 0
            ]
            if len(filled_components) > 1:
                self.main_window.info_dialog(
                    "Erro", "Por favor, preencha apenas um campo de componente."
                )
                return

            # Calculate total weight based on the provided component weight and its percentage
            if milho_weight:
                total_weight = milho_weight * 100 / milho_percentage
            elif soja_weight:
                total_weight = soja_weight * 100 / soja_percentage
            elif trigo_weight:
                total_weight = trigo_weight * 100 / trigo_percentage
            elif nucleo_weight:
                total_weight = nucleo_weight * 100 / nucleo_percentage
            elif calcario_weight:
                total_weight = calcario_weight * 100 / calcario_percentage

            if total_weight > 0:
                other_milho_weight = (
                    (milho_percentage * total_weight) / 100
                    if not milho_weight
                    else milho_weight
                )
                other_soja_weight = (
                    (soja_percentage * total_weight) / 100
                    if not soja_weight
                    else soja_weight
                )
                other_trigo_weight = (
                    (trigo_percentage * total_weight) / 100
                    if not trigo_weight
                    else trigo_weight
                )
                other_nucleo_weight = (
                    (nucleo_percentage * total_weight) / 100
                    if not nucleo_weight
                    else nucleo_weight
                )
                other_calcario_weight = (
                    (calcario_percentage * total_weight) / 100
                    if not calcario_weight
                    else calcario_weight
                )

                result_text = (
                    f"Peso Total da Ração: {total_weight:.2f} kg\n"
                    f"Milho: {other_milho_weight:.2f} kg\n"
                    f"Soja: {other_soja_weight:.2f} kg\n"
                    f"Trigo: {other_trigo_weight:.2f} kg\n"
                    f"Núcleo: {other_nucleo_weight:.2f} kg\n"
                    f"Calcário: {other_calcario_weight:.2f} kg"
                )

                self.main_window.info_dialog("Resultado", result_text)
            else:
                self.main_window.info_dialog(
                    "Erro", "Por favor, insira o peso total ou o peso de um componente."
                )

    def parse_formula(self, formula):
        # Parse the formula string to extract components
        components = {}
        for item in formula.split(", "):
            key, value = item.split(" ")
            components[key] = value
        return components

    def get_weight(self, value):
        try:
            return float(value)
        except ValueError:
            return 0


def main():
    return RacaoApp("RacaoApp", "com.example.racao")


if __name__ == "__main__":
    main().main_loop()
