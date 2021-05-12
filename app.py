from datetime import date
import textwrap

import mysql.connector
from mysql.connector import Error
import PySimpleGUI as sg

# -- Constants --#
today = date.today()
today_format = today.strftime("%B %d, %Y")


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
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# -- GUI --#
def dashboard_main(connection):
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

    top_banner = [[sg.Text('Al Rental' + ' ' * 64, font='Any 20', background_color=DARK_HEADER_COLOR),
                   sg.Text(today_format, font='Any 20', background_color=DARK_HEADER_COLOR)]]

    block_2 = [[sg.Text('Lookup', font='Any 20')],
               [sg.Text('Customer ID', size=(10, 1)), sg.InputText(key='-LOOKUP_ID-')],
               [sg.Button('Get')]]

    block_3 = [[sg.Text('Update Customer', font='Any 20')],
               [sg.Text('First Name', size=(10, 1)), sg.InputText(key='-FIRSTNAME-')],
               [sg.Text('Last Name', size=(10, 1)), sg.InputText(key='-LASTNAME-')],
               [sg.Text('Phone', size=(10, 1)), sg.InputText(key='-PHONE-')],
               [sg.Text('Email', size=(10, 1)), sg.InputText(key='-EMAIL-')],
               [sg.Text('Credit Card', size=(10, 1)), sg.InputText(key='-CREDIT_CARD-')],
               [sg.Button('Update'), sg.Button('Delete')]]

    block_4 = [[sg.Text('Add Customers', font='Any 20')],
               [sg.Text('First Name', size=(10, 1)), sg.InputText(key='-NEW_FIRSTNAME-')],
               [sg.Text('Last Name', size=(10, 1)), sg.InputText(key='-NEW_LASTNAME-')],
               [sg.Text('Phone', size=(10, 1)), sg.InputText(key='-NEW_PHONE-')],
               [sg.Text('Email', size=(10, 1)), sg.InputText(key='-NEW_EMAIL-')],
               [sg.Text('Credit Card', size=(10, 1)), sg.InputText(key='-NEW_CREDIT_CARD-')],
               [sg.Button('Add User'), sg.Button('Clear'), sg.Button('Exit')]]

    layout = [[sg.Column(top_banner, size=(960, 60), pad=(0, 0), background_color=DARK_HEADER_COLOR)],
              [sg.Column([[sg.Column(block_2, size=(450, 150), pad=BPAD_LEFT_INSIDE)],
                          [sg.Column(block_3, size=(450, 200), pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT,
                         background_color=BORDER_COLOR),
               sg.Column(block_4, size=(450, 370), pad=BPAD_RIGHT)]]

    window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0, 0), background_color=BORDER_COLOR,
                       no_titlebar=True, grab_anywhere=True)

    while True:  # Event Loop
        event, values = window.read()

        if event == 'Get':
            get_id = values['-LOOKUP_ID-']
            window.close()
            dashboard_get_customer(connection, get_id)
            break

        if event == 'Clear':
            window.close()
            dashboard_main(connection)
            break

        if event == 'Add User':
            add = '''
                INSERT INTO customer(first_name, last_name, phone_no, email, credit_card) 
                VALUES(%s, %s, %s, %s, %s);
                ''' % (values['-NEW_FIRSTNAME-'], values['-NEW_LASTNAME-'], values['-NEW_PHONE-'],
                       values['-NEW_EMAIL-'], values['-NEW_CREDIT_CARD-'])

            print(add)
            execute_query(connection, add)
            window.close()
            dashboard_main(connection)
            break

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()


def dashboard_get_customer(connection, get_id):
    q1 = "SELECT * FROM customer WHERE customer_id = '%s'" % get_id
    print(q1)

    results = read_query(connection, q1)

    for row in results:
        customer_id = row[0]
        first_name = row[1]
        last_name = row[2]
        phone = row[3]
        email = row[4]
        credit_card = row[5]

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

    top_banner = [[sg.Text('Al Rental' + ' ' * 64, font='Any 20', background_color=DARK_HEADER_COLOR),
                   sg.Text(today_format, font='Any 20', background_color=DARK_HEADER_COLOR)]]

    block_2 = [[sg.Text('Lookup', font='Any 20')],
               [sg.Text('Customer ID', size=(10, 1)), sg.InputText(customer_id, key='-LOOKUP_ID-')],
               [sg.Button('Get')]]

    block_3 = [[sg.Text('Update Customer', font='Any 20')],
               [sg.Text('First Name', size=(10, 1)), sg.InputText(first_name, key='-FIRSTNAME-')],
               [sg.Text('Last Name', size=(10, 1)), sg.InputText(last_name, key='-LASTNAME-')],
               [sg.Text('Phone', size=(10, 1)), sg.InputText(phone, key='-PHONE-')],
               [sg.Text('Email', size=(10, 1)), sg.InputText(email, key='-EMAIL-')],
               [sg.Text('Credit Card', size=(10, 1)), sg.InputText(credit_card, key='-CREDIT_CARD-')],
               [sg.Button('Update'), sg.Button('Delete')]]

    block_4 = [[sg.Text('Add Customers', font='Any 20')],
               [sg.Text('First Name', size=(10, 1)), sg.InputText(key='-NEW_FIRSTNAME-')],
               [sg.Text('Last Name', size=(10, 1)), sg.InputText(key='-NEW_LASTNAME-')],
               [sg.Text('Phone', size=(10, 1)), sg.InputText(key='-NEW_PHONE-')],
               [sg.Text('Email', size=(10, 1)), sg.InputText(key='-NEW_EMAIL-')],
               [sg.Text('Credit Card', size=(10, 1)), sg.InputText(key='-NEW_CREDIT_CARD-')],
               [sg.Button('Add User'), sg.Button('Clear'), sg.Button('Exit')]]

    layout = [[sg.Column(top_banner, size=(960, 60), pad=(0, 0), background_color=DARK_HEADER_COLOR)],
              [sg.Column([[sg.Column(block_2, size=(450, 150), pad=BPAD_LEFT_INSIDE)],
                          [sg.Column(block_3, size=(450, 200), pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT,
                         background_color=BORDER_COLOR),
               sg.Column(block_4, size=(450, 370), pad=BPAD_RIGHT)]]

    window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0, 0), background_color=BORDER_COLOR,
                       no_titlebar=True, grab_anywhere=True)

    while True:  # Event Loop
        event, values = window.read()

        if event == 'Get':
            get_id = values['-LOOKUP_ID-']
            window.close()
            dashboard_get_customer(connection, get_id)
            break

        if event == 'Clear':
            window.close()
            dashboard_main(connection)
            break

        if event == 'Delete':
            delete_course = '''
            DELETE FROM customer
            WHERE customer_id = '%s';
            ''' % get_id
            window.close()
            confirm_Delete(get_id, connection, delete_course)
            break

        if event == 'Update':
            update = '''
            UPDATE customer 
            SET 
            first_name = '%s', last_name = '%s', phone_no = '%s', email = '%s', credit_card = '%s' 
            WHERE customer_id = %s;
            ''' % (values['-FIRSTNAME-'], values['-LASTNAME-'], values['-PHONE-'],
                   values['-EMAIL-'], values['-CREDIT_CARD-'], get_id)
            print(update)
            execute_query(connection, update)
            window.close()
            dashboard_get_customer(connection, get_id)
            break

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()


def confirm_Delete(customer_id, connection, delete):
    window = sg.Window('Confirm Action',
                       [[sg.Text('Are you sure you want to delete customer_id %s' % customer_id)],
                        [sg.OK(), sg.Cancel()]])
    event, values = window.read()

    if event != 'OK':
        window.close()
        dashboard_get_customer(connection, customer_id)

    else:
        execute_query(connection, delete)
        window.close()
        dashboard_main(connection)


# -- MAIN -- #
connection = create_db_connection("localhost", "root", 'mypassword', 'al_rentals')
dashboard_main(connection)
