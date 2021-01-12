# Internal imports
from check_media import *
from zettel_listbox import *

# External imports
import PySimpleGUI as sg
from tkinter.simpledialog import askinteger


def check_media_menu():
    asset_Links, unused_assets, z_sans_ID, untitled_z, untagged_z = check_media()
    broken_link_z = asset_Links.get_broken()
    window = create_check_media_menu(broken_link_z, unused_assets, z_sans_ID, untitled_z, untagged_z)
    while True:
        event, values = window.read()

        # If the user closes the window or clicks 'Close'.
        if event == sg.WIN_CLOSED or event == '-close-':
            window.close()
            return

        handle_check_media_menu_event(event, values, window, broken_link_z, unused_assets, z_sans_ID, untitled_z, untagged_z)


def create_check_media_menu(broken_link_z, unused_assets, z_sans_ID, untitled_z, untagged_z):
    tab_list = []
    if len(unused_assets):
        layout = create_asset_table_layout(unused_assets, '-unused_assets-')
        tab_list += [sg.Tab('Unused assets', layout)]
    if len(broken_link_z):
        layout = create_zettel_listbox_layout(broken_link_z.links, '-broken_links-')
        layout += [[sg.Text('These buttons are for the zettels that contain the broken asset links.')]]
        tab_list += [sg.Tab('Broken asset links', layout)]
    if len(z_sans_ID):
        layout = create_zettel_listbox_layout(z_sans_ID.links, '-z_sans_ID-')
        tab_list += [sg.Tab('Zettels without IDs', layout)]
    if len(untitled_z):
        layout = create_zettel_listbox_layout(untitled_z.links, '-untitled_z-')
        tab_list += [sg.Tab('Zettels without titles', layout)]
    if len(untagged_z):
        layout = create_zettel_listbox_layout(untagged_z.links, '-untagged_z-')
        tab_list += [sg.Tab('Zettels without tags', layout)]

    layout = []
    if len(tab_list) == 0:
        layout = [[sg.Text('All\'s well.')],
                  [sg.Text('Could not find any unused assets, broken asset links,')],
                  [sg.Text('or zettels without IDs, titles, or tags.')]]
    else:
        layout += [[sg.TabGroup([tab_list])]]

    layout += [[sg.HorizontalSeparator(pad=(0, 8))],
               [sg.Button('Close', key='-close-')]]

    return sg.Window('Check media', layout)


def create_asset_table_layout(assets, key_name):
    data = format_asset_data(assets)
    total_bytes = format_bytes(sum(assets.values()))
    layout = [[sg.Table(key=key_name,
                        headings=['asset name', 'size'],
                        values=data,
                        num_rows=6,
                        row_height=20,
                        auto_size_columns=True,
                        max_col_width=100,
                        justification='left')],
              [sg.Button('Open', key='-open_' + key_name[1:]),
               sg.Button('Move', key='-move_' + key_name[1:]),
               sg.Button('Delete', key='-delete_' + key_name[1:]),
               sg.Button('Show in file browser', key='-show_' + key_name[1:]),
               sg.Text(f'       Total bytes: {total_bytes}')]]

    return layout


# Return a list of lists of asset names and their memory sizes.
def format_asset_data(assets):
    data = []
    for path, Bytes in assets.items():
        name = os.path.split(path)[-1]
        Bytes = format_bytes(Bytes)
        data += [[name, Bytes]]

    return data


def handle_check_media_menu_event(event, values, window, broken_link_z, unused_assets, z_sans_ID, untitled_z, untagged_z):
    if event.endswith('_unused_assets-'):
        handle_asset_table_event(event, window, values['-unused_assets-'], unused_assets)
        window['-unused_assets-'].update(format_asset_data(unused_assets))
    elif event.endswith('_broken_links-'):
        handle_zettel_listbox_event(event, window, values['-broken_links-'], broken_link_z)
        window['-broken_links-'].update(broken_link_z.links)
    elif event.endswith('_z_sans_ID-'):
        handle_zettel_listbox_event(event, window, values['-z_sans_ID-'], z_sans_ID)
        window['-z_sans_ID-'].update(z_sans_ID.links)
    elif event.endswith('_untitled_z-'):
        handle_zettel_listbox_event(event, window, values['-untitled_z-'], untitled_z)
        window['-untitled_z-'].update(untitled_z.links)
    elif event.endswith('_untagged_z-'):
        handle_zettel_listbox_event(event, window, values['-untagged_z-'], untagged_z)
        window['-untagged_z-'].update(untagged_z.links)


def handle_asset_table_event(event, window, selected_asset_names, unused_assets):
    selected_paths = get_selected_asset_paths(selected_asset_names, unused_assets)

    if event.startswith('-open'):
        for path in selected_paths:
            if os.path.exists(path):
                webbrowser.open('file://' + path)
            else:
                sg.Popup(f'File not found: {path}', title='Error')
                del unused_assets[path]
    elif event.startswith('-show'):
        for path in selected_paths:
            if os.path.exists(path):
                show_file(path)
            else:
                sg.Popup(f'File not found: {path}', title='Check media')
                del unused_assets[path]
    elif event.startswith('-delete'):
        number = len(selected_paths)
        entry = askinteger('Check media', f'Are you sure you want to delete the selected files? Enter {number}, the number of selected files, to confirm:')
        if entry != number:
            sg.Popup('Canceled deletion.', title='Check media')
        else:
            for path in list(selected_paths):
                if os.path.exists(path):
                    delete_unused_asset(path)
                    del unused_assets[path]
                else:
                    sg.Popup(f'File not found: {path}', title='Error')
                    del unused_assets[path]
            sg.Popup('Selected assets sent to the recycle bin.', title='Check media')
    elif event.startswith('-move'):
        destination = askdirectory(title='Select the destination folder.', mustexist=True)
        if destination != '':
            for path in list(selected_paths):
                if os.path.exists(path):
                    new_path = os.path.join(destination, os.path.split(path)[-1])
                    os.rename(path, new_path)
                    unused_assets.update({new_path: unused_assets[path]})
                    del unused_assets[path]
                else:
                    sg.Popup(f'File not found: {path}', title='Error')
                    del unused_assets[path]
            sg.Popup(f'Selected assets moved to {destination}', title='Check media')


# Return a list of paths selected in a table.
def get_selected_asset_paths(selected_asset_names, unused_assets):
    if len(selected_asset_names) == 0:
        return unused_assets.keys()

    selected_asset_paths = []
    for name in selected_asset_names:
        for path in unused_assets.keys():
            if path.endswith(name):
                selected_asset_paths.append(path)
                break

    return selected_asset_paths


if __name__ == '__main__':
    check_media_menu()
