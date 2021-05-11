import mysql.connector
from mysql.connector import Error
import PySimpleGUI as sg


# -- database connections -- #
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


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
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


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


# -- GUI --#
def customer_window():
    theme_dict = {'BACKGROUND': '#2B475D',
                  'TEXT': '#FFFFFF',
                  'INPUT': '#F2EFE8',
                  'TEXT_INPUT': '#000000',
                  'SCROLL': '#F2EFE8',
                  'BUTTON': ('#000000', '#C2D4D8'),
                  'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                  'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

    # sg.theme_add_new('Dashboard', theme_dict)
    sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
    sg.theme('Dashboard')

    BORDER_COLOR = '#C7D5E0'
    DARK_HEADER_COLOR = '#1B2838'
    BPAD_LEFT = ((20, 10), (0, 10))
    BPAD_LEFT_INSIDE = (0, 10)
    BPAD_RIGHT = ((10, 20), (10, 20))

    top_banner = [[sg.Text('Dashboard' + ' ' * 64, font='Any 20', background_color=DARK_HEADER_COLOR),
                   sg.Text('Tuesday 9 June 2020', font='Any 20', background_color=DARK_HEADER_COLOR)]]

    block_2 = [[sg.Text('Customers', font='Any 20')],
               [sg.Button('Add New'), sg.Button('Update'), sg.Button('Delete'), sg.Button('Get')]]

    block_3 = [[sg.Text('Please enter your Name, Address, Phone')],
               [sg.Text('Name', size=(10, 1)), sg.InputText(key='-NAME-')],
               [sg.Text('Address', size=(10, 1)), sg.InputText(key='-ADDRESS-')],
               [sg.Text('Phone', size=(10, 1)), sg.InputText(key='-PHONE-')],
               [sg.Button('Submit'), sg.Button('Exit')]]

    block_4 = [[sg.Text('Block 4', font='Any 20')],
               [sg.T('make a selection')]]

    layout = [[sg.Column(top_banner, size=(960, 60), pad=(0, 0), background_color=DARK_HEADER_COLOR)],
              [sg.Column([[sg.Column(block_2, size=(450, 150), pad=BPAD_LEFT_INSIDE)],
                          [sg.Column(block_3, size=(450, 150), pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT,
                         background_color=BORDER_COLOR),
               sg.Column(block_4, size=(450, 320), pad=BPAD_RIGHT)]]

    window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0, 0), background_color=BORDER_COLOR,
                       no_titlebar=True, grab_anywhere=True)

    while True:  # Event Loop
        event, values = window.read()

        if event == 'Get':
            customer_window_get()
            break

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()


def customer_window_get():
    # -- Establish customer DB connection -- #
    q1 = """
               SELECT *
               FROM customer;
               """
    connection = create_db_connection("localhost", "root", 'mypassword', 'al_rentals')
    results = read_query(connection, q1)

    theme_dict = {'BACKGROUND': '#2B475D',
                  'TEXT': '#FFFFFF',
                  'INPUT': '#F2EFE8',
                  'TEXT_INPUT': '#000000',
                  'SCROLL': '#F2EFE8',
                  'BUTTON': ('#000000', '#C2D4D8'),
                  'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                  'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

    # sg.theme_add_new('Dashboard', theme_dict)
    sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
    sg.theme('Dashboard')

    BORDER_COLOR = '#C7D5E0'
    DARK_HEADER_COLOR = '#1B2838'
    BPAD_LEFT = ((20, 10), (0, 10))
    BPAD_LEFT_INSIDE = (0, 10)
    BPAD_RIGHT = ((10, 20), (10, 20))

    top_banner = [[sg.Text('Dashboard' + ' ' * 64, font='Any 20', background_color=DARK_HEADER_COLOR),
                   sg.Text('Tuesday 9 June 2020', font='Any 20', background_color=DARK_HEADER_COLOR)]]

    block_2 = [[sg.Text('Customers', font='Any 20')],
               [sg.Button('Add New'), sg.Button('Update'), sg.Button('Delete'), sg.Button('Get')]]

    block_3 = [[sg.Text('Please enter your Name, Address, Phone')],
               [sg.Text('Name', size=(10, 1)), sg.InputText(key='-NAME-')],
               [sg.Text('Address', size=(10, 1)), sg.InputText(key='-ADDRESS-')],
               [sg.Text('Phone', size=(10, 1)), sg.InputText(key='-PHONE-')],
               [sg.Button('Submit'), sg.Button('Exit')]]

    block_4 = [[sg.Text('Block 4', font='Any 20')],
               [sg.T(results)]]

    layout = [[sg.Column(top_banner, size=(960, 60), pad=(0, 0), background_color=DARK_HEADER_COLOR)],
              [sg.Column([[sg.Column(block_2, size=(450, 150), pad=BPAD_LEFT_INSIDE)],
                          [sg.Column(block_3, size=(450, 150), pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT,
                         background_color=BORDER_COLOR),
               sg.Column(block_4, size=(450, 320), pad=BPAD_RIGHT)]]

    window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0, 0), background_color=BORDER_COLOR,
                       no_titlebar=True, grab_anywhere=True)

    while True:  # Event Loop
        event, values = window.read()

        if event == 'Get':
            q1 = """
            SELECT *
            FROM customer;
            """
            results = read_query(connection, q1)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()


customer_window()
