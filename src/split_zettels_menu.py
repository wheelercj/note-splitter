# Internal imports
from split_zettels import *
from common import get_zettel_links

# External imports
import PySimpleGUI as sg
import webbrowser


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

        respond_to_split_menu_event(event, values, window, zettels_to_split, zettel_links)


def create_split_menu(zettel_links):
    layout = [[sg.Combo(['#', '##', '###', '####', '#####', '######'], key='-header_level-', default_value='####', size=(8, 20), pad=(5, 15), readonly=True), sg.Text('Header level to split by')],
              [sg.Text('Zettels with the tag "#split":')],
              [sg.Listbox(zettel_links, size=(80, 6), key='-zettels_to_split-')],
              [sg.Button('Split all', key='-split_all-'), sg.Button('Split selected', key='-split_selected-')],
              [sg.HorizontalSeparator(pad=(0, 8))],
              [sg.Cancel()]]

    return sg.Window('Split zettels', layout)


def respond_to_split_menu_event(event, values, window, zettels_to_split, zettel_links):
    header_level = values['-header_level-'].count('#')

    if values['-header_level-'] == '':
        sg.Popup('Please select a header level to split by.', title='Error')
    elif event == '-split_all-':
        window.close()
        new_zettels, z_without_h_links, z_without_h_paths = split_zettels(zettels_to_split, header_level)
        display_results_menu(new_zettels, z_without_h_links, z_without_h_paths, header_level)
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

            new_zettels, z_without_h_links, z_without_h_paths = split_zettels(chosen_zettel_paths, header_level)
            display_results_menu(new_zettels, z_without_h_links, z_without_h_paths, header_level)


def display_results_menu(new_zettels, z_without_h_links, z_without_h_paths, header_level):
    window = create_results_menu(new_zettels, z_without_h_links, z_without_h_paths, header_level)
    while True:
        event, values = window.read()

        # If the user closes the window or clicks 'Close'.
        if event == sg.WIN_CLOSED or event == '-close-':
            window.close()
            return

        respond_to_results_menu_event(event, values, new_zettels, z_without_h_links, z_without_h_paths)


def create_results_menu(new_zettels, z_without_h_links, z_without_h_paths, header_level):
    layout = []

    if len(new_zettels.links):
        layout.append([sg.Text('New zettels:')])
        layout.append([sg.Listbox(new_zettels.links, size=(80, 6), key='-new_zettels-')])
        layout.append([sg.Button('Open selected', key='-open_new-')])
    else:
        layout.append([sg.Text('No zettels were changed or created.')])

    layout.append([sg.HorizontalSeparator(pad=(0, 8))])

    if len(z_without_h_links):
        layout.append([sg.Text(f'Could not find a header of level {header_level} in zettels:')])
        layout.append([sg.Listbox(z_without_h_links, size=(80, 6), key='-without_header-')])
        layout.append([sg.Button('Open selected', key='-open_old-')])

    layout.append([sg.Text(' ')])
    layout.append([sg.Button('Close', key='-close-')])

    return sg.Window('Split zettels', layout)


def respond_to_results_menu_event(event, values, window, new_zettels, zettels_sans_h):
    if event.endswith('_new_z-'):
        paths = get_listbox_paths(values['-new_z-'], new_zettels)
        handle_subevent(event, window, paths, new_zettels)
        window['-new_z-'].update(new_zettels.links)
    elif event.endswith('_z_sans_h-'):
        paths = get_listbox_paths(values['-z_sans_h-'], zettels_sans_h)
        handle_subevent(event, window, paths, zettels_sans_h)
        window['-z_sans_h-'].update(zettels_sans_h.links)


def handle_subevent(event, window, paths, zettels):
    if event.startswith('-open'):
        for path in paths:
            if os.path.exists(path):
                webbrowser.open('file://' + path)
            else:
                sg.Popup(f'File not found: {path}')
                zettels.remove_path(path)
    elif event.startswith('-show'):
        for path in paths:
            if os.path.exists(path):
                show_file(path)
            else:
                sg.Popup(f'File not found: {path}')
                zettels.remove_path(path)
    elif event.startswith('-move'):
        destination = askdirectory(title='Select the destination folder.', mustexist=True)
        if destination != '':
            for path in paths:
                new_path = os.path.join(destination, os.path.split(path)[-1])
                os.rename(path, new_path)  # TODO: update any relative file links in the zettel.
                zettels.repath(path, new_path)


def get_listbox_paths(selected_links, listbox_zettels):
    # Determine which links to get the paths of.
    if len(selected_links) == 0:
        return listbox_zettels.paths

    # Convert the links to paths.
    selected_paths = []
    for link in selected_links:
        path = listbox_zettels.path_of_link(link)
        selected_paths.append(path)

    return selected_paths


if __name__ == '__main__':
    split_zettels_menu()
