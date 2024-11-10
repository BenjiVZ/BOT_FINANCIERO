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

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormValidationAction
import sqlite3
import os

# Ruta absoluta a la base de datos
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'C:/Users/Benjamin/Desktop/BOT_FINANCIERO/Django/db.sqlite3'))

# Al inicio del archivo, después de las importaciones
def verificar_base_datos():
    try:
        if not os.path.exists(DB_PATH):
            raise Exception(f"Base de datos no encontrada en: {DB_PATH}")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar si las tablas necesarias existen
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN 
            ('chatbot_app_cuenta', 'chatbot_app_transaccion', 'chatbot_app_categoria')
        """)
        tablas = cursor.fetchall()
        tablas_encontradas = [t[0] for t in tablas]
        
        tablas_requeridas = ['chatbot_app_cuenta', 'chatbot_app_transaccion', 'chatbot_app_categoria']
        tablas_faltantes = [t for t in tablas_requeridas if t not in tablas_encontradas]
        
        if tablas_faltantes:
            raise Exception(f"Faltan las siguientes tablas: {', '.join(tablas_faltantes)}")
            
        conn.close()
        return True
    except sqlite3.Error as e:
        raise Exception(f"Error de SQLite: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

class ActionConsultarSaldo(Action):
    def name(self) -> Text:
        return "action_consultar_saldo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Verificar si la tabla existe
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='chatbot_app_cuenta'
            """)
            if not cursor.fetchone():
                dispatcher.utter_message(text="Error: La tabla de cuentas no existe en la base de datos.")
                return []

            cursor.execute("""
                SELECT numero_cuenta, saldo, moneda 
                FROM chatbot_app_cuenta
            """)
            cuentas = cursor.fetchall()
            
            if not cuentas:
                dispatcher.utter_message(text="No hay cuentas registradas en el sistema.")
                return []
                
            mensaje = "Saldos de tus cuentas:\n"
            for cuenta in cuentas:
                mensaje += f"Cuenta {cuenta[0]}: {cuenta[1]} {cuenta[2]}\n"
            
            dispatcher.utter_message(text=mensaje)
            
        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Error de base de datos: {str(e)}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error inesperado: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
        return []

class ExpenseForm(Action):
    def name(self) -> Text:
        return "expense_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []

class ActionSaveExpense(Action):
    def name(self) -> Text:
        return "action_save_expense"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cantidad = tracker.get_slot("cantidad")
        categoria = tracker.get_slot("categoria")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO chatbot_app_transaccion (fecha, monto, tipo, categoria_id, descripcion)
                VALUES (date('now'), ?, 'GASTO', (SELECT id FROM chatbot_app_categoria WHERE nombre = ?), ?)
            """, (cantidad, categoria, f"Gasto en {categoria}"))
            conn.commit()
            dispatcher.utter_message(text=f"Gasto de {cantidad} registrado en categoría {categoria}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error al guardar el gasto: {str(e)}")
        finally:
            conn.close()
        return []

class ActionConsultarEstadoCuenta(Action):
    def name(self) -> Text:
        return "action_consultar_estado_cuenta"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Verificar si las tablas existen
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND (name='chatbot_app_transaccion' OR name='chatbot_app_categoria')
            """)
            tablas = cursor.fetchall()
            if len(tablas) < 2:
                dispatcher.utter_message(text="Error: No se encontraron todas las tablas necesarias.")
                return []

            cursor.execute("""
                SELECT t.fecha, t.monto, t.tipo, c.nombre, t.descripcion
                FROM chatbot_app_transaccion t
                JOIN chatbot_app_categoria c ON t.categoria_id = c.id
                ORDER BY t.fecha DESC
                LIMIT 5
            """)
            transacciones = cursor.fetchall()
            
            if not transacciones:
                dispatcher.utter_message(text="No hay transacciones registradas.")
                return []
            
            mensaje = "Últimas 5 transacciones:\n"
            for t in transacciones:
                mensaje += f"- {t[0]}: {t[1]} ({t[2]}) - {t[3]} - {t[4]}\n"
            
            dispatcher.utter_message(text=mensaje)
            
        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"Error de base de datos: {str(e)}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error inesperado: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
        return []

class ActionVerHistorial(Action):
    def name(self) -> Text:
        return "action_ver_historial"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT c.nombre, SUM(t.monto) as total
                FROM chatbot_app_transaccion t
                JOIN chatbot_app_categoria c ON t.categoria_id = c.id
                GROUP BY c.nombre
            """)
            totales = cursor.fetchall()
            
            mensaje = "Totales por categoría:\n"
            for total in totales:
                mensaje += f"- {total[0]}: {total[1]}\n"
            
            dispatcher.utter_message(text=mensaje)
        except Exception as e:
            dispatcher.utter_message(text=f"Error al consultar historial: {str(e)}")
        finally:
            conn.close()
        return []

class ActionValidarGastosRatio(Action):
    def name(self) -> Text:
        return "action_validar_gastos_ratio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT SUM(monto) as total_gastos
                FROM chatbot_app_transaccion
                WHERE tipo = 'GASTO'
            """)
            total_gastos = cursor.fetchone()[0] or 0
            
            cursor.execute("""
                SELECT presupuesto_mensual
                FROM chatbot_app_configuracion
                LIMIT 1
            """)
            presupuesto = cursor.fetchone()[0] or 0
            
            if total_gastos > presupuesto * 0.8:
                return [{"event": "slot", "name": "alerta_gastos", "value": True}]
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error al validar gastos: {str(e)}")
        finally:
            conn.close()
        return []

class ValidateExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_expense_form"

    def validate_cantidad(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
            cantidad = float(slot_value)
            if cantidad <= 0:
                dispatcher.utter_message(text="La cantidad debe ser mayor a 0")
                return {"cantidad": None}
            return {"cantidad": cantidad}
        except ValueError:
            dispatcher.utter_message(text="Por favor ingresa un número válido")
            return {"cantidad": None}

    def validate_categoria(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT nombre FROM chatbot_app_categoria")
            categorias = [row[0].lower() for row in cursor.fetchall()]
            
            if slot_value.lower() in categorias:
                return {"categoria": slot_value}
            else:
                dispatcher.utter_message(text=f"Categoría no válida. Las categorías disponibles son: {', '.join(categorias)}")
                return {"categoria": None}
        finally:
            conn.close()
