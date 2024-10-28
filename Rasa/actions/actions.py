# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List

class ActionRegistrarIngreso(Action):
    def name(self) -> Text:
        return "action_registrar_ingreso"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cantidad = next(tracker.get_latest_entity_values("cantidad"), None)
        
        if cantidad is not None:
            try:
                cantidad = float(cantidad)
                ingresos_actuales = tracker.get_slot("ingresos") or 0.0
                nuevo_ingreso = ingresos_actuales + cantidad
                dispatcher.utter_message(text=f"Ingreso registrado: {cantidad}. Total ingresos: {nuevo_ingreso}")
                return [SlotSet("ingresos", nuevo_ingreso)]
            except ValueError:
                dispatcher.utter_message(text="Por favor, ingrese una cantidad válida para el ingreso.")
                return []
        else:
            dispatcher.utter_message(text="No se pudo registrar el ingreso. Intente nuevamente especificando la cantidad.")
            return []

class ActionRegistrarGasto(Action):
    def name(self) -> Text:
        return "action_registrar_gasto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cantidad = next(tracker.get_latest_entity_values("cantidad"), None)
        categoria = next(tracker.get_latest_entity_values("categoria"), None)
        
        if cantidad is not None and categoria is not None:
            try:
                cantidad = float(cantidad)
                gastos_actuales = tracker.get_slot("gastos") or []
                nuevo_gasto = {"cantidad": cantidad, "categoria": categoria}
                gastos_actuales.append(nuevo_gasto)
                dispatcher.utter_message(text=f"Gasto registrado: {cantidad} en {categoria}")
                return [SlotSet("gastos", gastos_actuales)]
            except ValueError:
                dispatcher.utter_message(text="Por favor, ingrese una cantidad válida para el gasto.")
                return []
        else:
            dispatcher.utter_message(text="No se pudo registrar el gasto. Asegúrese de especificar tanto la cantidad como la categoría.")
            return []

class ActionSolicitarResumen(Action):
    def name(self) -> Text:
        return "action_solicitar_resumen"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ingresos = tracker.get_slot("ingresos") or 0.0
        gastos = tracker.get_slot("gastos") or []
        total_gastos = sum(g["cantidad"] for g in gastos)
        balance = ingresos - total_gastos

        if balance < ingresos * 0.2:  # umbral del 20% de ahorro
            categoria_sugerida = min(gastos, key=lambda x: x["cantidad"])["categoria"] if gastos else "ninguna"
            dispatcher.utter_message(
                text=f"Tu balance es de {balance}. Has gastado {total_gastos}. Para ahorrar más, intenta reducir los gastos en {categoria_sugerida}."
            )
        else:
            dispatcher.utter_message(text=f"Tu balance es de {balance}. Has gastado {total_gastos} este mes.")
        
        return []

class ActionValidarCantidad(Action):
    def name(self):
        return "action_validar_cantidad"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        cantidad = tracker.get_slot("cantidad")
        
        if cantidad and float(cantidad) < 0:
            dispatcher.utter_message(text="La cantidad no puede ser negativa. Por favor, ingrese un valor válido.")
            return [SlotSet("cantidad", None)]
        
        return []

class ActionValidarGastosRatio(Action):
    def name(self):
        return "action_validar_gastos_ratio"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        gastos_ratio = tracker.get_slot("gastos_ratio")
        
        if gastos_ratio and float(gastos_ratio) > 0.8:
            dispatcher.utter_message(text="Se recomienda reducir los gastos. Ha alcanzado un alto porcentaje de sus ingresos.")
        
        return []
