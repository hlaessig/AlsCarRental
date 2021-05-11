import mysql.connector
from mysql.connector import Error
import PySimpleGUI as sg


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def layout0():
    layout = [[sg.Button(i) for i in range(4)]]     # A list of buttons is created

    window = sg.Window('Generated Layouts', layout)

    event, values = window.read()

    print(event, values)
    window.close()


layout0()
connection = create_server_connection("localhost", "root", 'mypassword')
