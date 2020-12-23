# Internal imports
from split_zettels import *
from zettel_listbox import *
from common import get_zettel_links

# External imports
import PySimpleGUI as sg


def split_zettels_menu():
    zettels_to_split = get_zettels_to_split()

    if len(zettels_to_split) == 0:
        sg.Popup('Could not find any zettels with the tag "#split".', title='Error')
        return

    zettel_links = get_zettel_links(zettels_to_split)
    window = create_split_menu(zettel_links)
    while True:
        event, values = window.read()

        # If the user closes the window or clicks 'Cancel'.
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            return

        handle_split_menu_event(event, values, window, zettels_to_split, zettel_links)


def create_split_menu(zettel_links):
    layout = [[sg.Combo(['#', '##', '###', '####', '#####', '######'], key='-header_level-', default_value='####', size=(8, 20), pad=(5, 15), readonly=True), sg.Text('Header level to split by')],
              [sg.Text('Zettels with the tag "#split":')],
              [sg.Listbox(zettel_links, size=(80, 6), key='-zettels_to_split-')],
              [sg.Button('Split all', key='-split_all-'), sg.Button('Split selected', key='-split_selected-')],
              [sg.HorizontalSeparator(pad=(0, 8))],
              [sg.Cancel()]]

    return sg.Window('Split zettels', layout)


def handle_split_menu_event(event, values, window, zettels_to_split, zettel_links):
    header_level = values['-header_level-'].count('#')

    if values['-header_level-'] == '':
        sg.Popup('Please select a header level to split by.', title='Error')
    elif event == '-split_all-':
        window.close()
        new_zettels, zettels_sans_h = split_zettels(zettels_to_split, header_level)
        display_results_menu(new_zettels, zettels_sans_h, header_level)
    elif event == '-split_selected-':
        if len(values['-zettels_to_split-']) == 0:
            sg.Popup('Select zettels to split or click "split all".')
        else:
            window.close()
            # The user did not choose to split all the zettels that contain '#split',
            # so get the list of paths of those chosen zettels.
            chosen_zettel_paths = []
            for zettel_link in values['-zettels_to_split-']:
                i = zettel_links.index(zettel_link)
                # The lists zettels_to_split and zettel_links are parallel.
                chosen_zettel_paths.append(zettels_to_split[i])

            new_zettels, zettels_sans_h = split_zettels(chosen_zettel_paths, header_level)
            display_results_menu(new_zettels, zettels_sans_h, header_level)


def display_results_menu(new_zettels, zettels_sans_h, header_level):
    window = create_results_menu(new_zettels, zettels_sans_h, header_level)
    while True:
        event, values = window.read()

        # If the user closes the window or clicks 'Close'.
        if event == sg.WIN_CLOSED or event == '-close-':
            window.close()
            return

        handle_results_menu_event(event, values, window, new_zettels, zettels_sans_h)


def create_results_menu(new_zettels, zettels_sans_h, header_level):
    layout = []

    if len(new_zettels.links):
        layout += [[sg.Text('New zettels:')]]
        layout += create_zettel_listbox_layout(new_zettels.links, '-new_z-')
    else:
        layout += [[sg.Text('No zettels were changed or created.')]]

    if len(zettels_sans_h.links):
        layout += [[sg.HorizontalSeparator(pad=(0, 8))],
                   [sg.Text(f'Could not find a header of level {header_level} in zettels:')]]
        layout += create_zettel_listbox_layout(zettels_sans_h.links, '-z_sans_h-')

    layout += [[sg.HorizontalSeparator(pad=(0, 8))],
               [sg.Button('Close', key='-close-')]]

    return sg.Window('Split zettels', layout)


def handle_results_menu_event(event, values, window, new_zettels, zettels_sans_h):
    if event.endswith('_new_z-'):
        paths = get_zettel_listbox_paths(values['-new_z-'], new_zettels)
        handle_zettel_listbox_event(event, window, paths, new_zettels)
        window['-new_z-'].update(new_zettels.links)
    elif event.endswith('_z_sans_h-'):
        paths = get_zettel_listbox_paths(values['-z_sans_h-'], zettels_sans_h)
        handle_zettel_listbox_event(event, window, paths, zettels_sans_h)
        window['-z_sans_h-'].update(zettels_sans_h.links)


if __name__ == '__main__':
    split_zettels_menu()
