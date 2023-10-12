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

import psycopg2
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, List, Dict, Any
from unidecode import unidecode

class ActionGetPrice(Action):
    def name(self):
        return "action_get_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        try:
            # Thông tin kết nối đến PostgreSQL
            dbname = 'postgres'
            user = 'postgres'
            password = 'root'
            host = 'localhost'  # Thay đổi host nếu cần

            # Tạo kết nối đến cơ sở dữ liệu
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
            try:
                product_name = tracker.latest_message.get('entities', [{'entity': 'product_name', 'value': None}])[0]['value']
                print(product_name)
            except Exception as e:
                print(str(e))

            if(product_name is not None):
            
                # Tạo một con trỏ đến cơ sở dữ liệu
                cursor = conn.cursor()
                # Thực hiện truy vấn SQL
                cursor.execute("SELECT name, price FROM product WHERE name ILIKE %s", ('%' + product_name + '%',))
                result = cursor.fetchall()

                listOfProduct = [list(tup) for tup in result]
                resultString = ""
                for product in listOfProduct:
                    price = "{:,.0f}".format(product[1]).replace(",", ".") + " ₫"
                    product[1] = price   
                    resultString += "- " + product[0] + ": " + product[1] + "\n"

                # Đóng con trỏ và kết nối
                cursor.close()
                conn.close()

                if result:
                    dispatcher.utter_message(f"Đây là giá của các mẫu '{product_name}': \n{resultString}")
                else:
                    dispatcher.utter_message(f"Không tìm thấy thông tin về sản phẩm '{product_name}'.")

                return []
            else: 
                dispatcher.utter_message("Xin vui lòng cung cấp tên sản phẩm.")

        except Exception as e:
            print(str(e))
            dispatcher.utter_message("Không tìm thấy sản phẩm. Vui lòng thử lại sau.")

        return [] 

class ActionGetDescription(Action):
    def name(self):
        return "action_get_description"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        try:
            # Thông tin kết nối đến PostgreSQL
            dbname = 'postgres'
            user = 'postgres'
            password = 'root'
            host = 'localhost'  # Thay đổi host nếu cần

            # Tạo kết nối đến cơ sở dữ liệu
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
            try:
                product_name = tracker.latest_message.get('entities', [{'entity': 'product_name', 'value': None}])[0]['value']
                print(product_name)
            except Exception as e:
                print(str(e))

            if(product_name is not None):
            
                # Tạo một con trỏ đến cơ sở dữ liệu
                cursor = conn.cursor()
                # Thực hiện truy vấn SQL
                cursor.execute("SELECT name, description FROM product WHERE name ILIKE %s", ('%' + product_name + '%',))
                result = cursor.fetchone()

                # Đóng con trỏ và kết nối
                cursor.close()
                conn.close()

                if result:
                    dispatcher.utter_message(f"Đây là thông tin về '{result[0]}': {result[1]}.")
                else:
                    dispatcher.utter_message(f"Không tìm thấy thông tin về sản phẩm '{product_name}'.")

                return []
            else: 
                dispatcher.utter_message("Xin vui lòng cung cấp tên sản phẩm.")

        except Exception as e:
            print(str(e))
            dispatcher.utter_message("Không tìm thấy sản phẩm. Vui lòng thử lại sau.")

        return [] 
    

class ActionGetStock(Action):
    def name(self):
        return "action_get_stock"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        try:
            # Thông tin kết nối đến PostgreSQL
            dbname = 'postgres'
            user = 'postgres'
            password = 'root'
            host = 'localhost'  # Thay đổi host nếu cần

            # Tạo kết nối đến cơ sở dữ liệu
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
            try:
                product_name = tracker.latest_message.get('entities', [{'entity': 'product_name', 'value': None}])[0]['value']
                print(product_name)
            except Exception as e:
                print(str(e))

            if(product_name is not None):
            
                # Tạo một con trỏ đến cơ sở dữ liệu
                cursor = conn.cursor()
                # Thực hiện truy vấn SQL

                cursor.execute("SELECT name, quantity FROM product WHERE name ILIKE %s", ('%' + product_name + '%',))

                result = cursor.fetchall()
                listOfProduct = [list(tup) for tup in result]
                resultString = ""
                for product in listOfProduct:
                    if(product[1] > 0):
                        resultString += "- " + product[0] + "\n"

                
                # Đóng con trỏ và kết nối
                cursor.close()
                conn.close()

                if (len(result) == 0):
                    dispatcher.utter_message(f"Không tìm thấy thông tin về sản phẩm '{product_name}'.")
                elif resultString:
                    dispatcher.utter_message(f"Đây là danh sách các mẫu '{product_name}' hiện vẫn còn hàng: \n{resultString}")
                else:
                    dispatcher.utter_message(f"Sản phẩm '{product_name}' hiện đã hết hàng. Xin hãy tìm kiếm các sản phẩm khác.")
                    
                return []
            else: 
                dispatcher.utter_message("Xin vui lòng cung cấp tên sản phẩm.")

        except Exception as e:
            print(str(e))
            dispatcher.utter_message("Không tìm thấy sản phẩm. Vui lòng thử lại sau.")

        return []
    



