# Internal imports
from common import show_file

# External imports
import os
import webbrowser
import PySimpleGUI as sg
from tkinter.filedialog import askdirectory


def create_zettel_listbox_layout(info_to_display, key_name):
    return [[sg.Listbox(info_to_display, size=(80, 6), key=key_name)],
            [sg.Button('Open', key='-open_' + key_name[1:]),
             sg.Button('Move', key='-move_' + key_name[1:]),
             sg.Button('Show in file browser', key='-show_' + key_name[1:])]]


# Parameter listbox_zettels must be a Zettels object with at least the paths and links.
def handle_zettel_listbox_event(event, window, selected_z_links, listbox_zettels):
    selected_paths = get_zettel_listbox_paths(selected_z_links, listbox_zettels)

    if event.startswith('-open'):
        for path in selected_paths:
            if os.path.exists(path):
                webbrowser.open('file://' + path)
            else:
                sg.Popup(f'File not found: {path}')
                listbox_zettels.remove_path(path)
    elif event.startswith('-show'):
        for path in selected_paths:
            if os.path.exists(path):
                show_file(path)
            else:
                sg.Popup(f'File not found: {path}')
                listbox_zettels.remove_path(path)
    elif event.startswith('-move'):
        destination = askdirectory(title='Select the destination folder.', mustexist=True)
        if destination != '':
            for path in selected_paths:
                if os.path.exists(path):
                    new_path = os.path.join(destination, os.path.split(path)[-1])
                    os.rename(path, new_path)  # TODO: update any relative file links in the zettel.
                    listbox_zettels.repath(path, new_path)
                else:
                    sg.Popup(f'File not found: {path}')
                    listbox_zettels.remove_path(path)


# Parameter listbox_zettels must be a Zettels object with at least the paths and links.
def get_zettel_listbox_paths(selected_z_links, listbox_zettels):
    # Determine which links to get the paths of.
    if len(selected_z_links) == 0:
        return listbox_zettels.paths

    # Convert the links to paths.
    selected_paths = []
    for link in selected_z_links:
        path = listbox_zettels.path_of_link(link)
        selected_paths.append(path)

    return selected_paths
