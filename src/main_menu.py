# Internal imports
from split_zettels_menu import split_zettels_menu
from check_media_menu import check_media_menu
from move_media_menu import move_media_menu
from help_menu import help_menu
from settings_menu import settings_menu

# External imports
import PySimpleGUI as sg


def main_menu():
    window = create_main_menu()
    while True:
        event, _ = window.read()

        if event == sg.WIN_CLOSED or event == 'exit':
            window.close()
            return

        window.Hide()
        respond_to_main_menu_event(event)
        window.UnHide()


def create_main_menu():
    layout = [[sg.Text('Mend', font=(20), pad=(40, 5))],
              [sg.Button('split zettels', size=(14, 1), pad=(40, 5))],
              [sg.Button('check media', size=(14, 1), pad=(40, 5))],
              [sg.Button('move media', size=(14, 1), pad=(40, 5))],
              [sg.HorizontalSeparator(pad=(0, 8))],
              [sg.Button('help', size=(14, 1), pad=(40, 5))],
              [sg.Button('settings', size=(14, 1), pad=(40, 5))],
              [sg.Button('exit', size=(14, 1), pad=(40, 5))],
              [sg.Text(' ' * 10)]]

    return sg.Window('Mend', layout)


def respond_to_main_menu_event(event):
    if event == 'split zettels':
        split_zettels_menu()
    elif event == 'check media':
        check_media_menu()
    elif event == 'move media':
        move_media_menu()
    elif event == 'help':
        help_menu()
    elif event == 'settings':
        settings_menu()


if __name__ == '__main__':
    main_menu()
