# Internal imports
from settings_menu import get_asset_types_str

# External imports
import textwrap
import webbrowser
import PySimpleGUI as sg


def help_menu():
    window = create_help_menu()
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok':
            window.close()
            return
        respond_to_menu_event(event)


def create_help_menu():
    guide_text = get_guide_text()
    about_text = get_about_text()
    license_text = get_license_text()

    guide_tab_layout = [[sg.Multiline(guide_text, size=(60, 28), write_only=True)],
                        [sg.Button('See the README', key='-README-')]]
    about_tab_layout = [[sg.Multiline(about_text, size=(60, 7), write_only=True)],
                        [sg.Button('See the README', key='-README-')],
                        [sg.Button('See the source code on GitHub', key='-source-')],
                        [sg.Button('Report a bug or request a feature', key='-issues-')],
                        [sg.Button('Discuss', key='-discuss-')]]
    license_tab_layout = [[sg.Multiline(license_text, size=(60, 28), write_only=True)]]

    layout = [[sg.TabGroup([[sg.Tab('Guide', guide_tab_layout),
                             sg.Tab('About', about_tab_layout),
                             sg.Tab('License', license_tab_layout)]])],
              [sg.Ok()]]

    return sg.Window('Mend', layout)


def get_guide_text():
    asset_types_str = get_asset_types_str()
    text = []
    text.append(textwrap.fill('Mend is an app that complements a locally-saved markdown-based zettelkasten (such as with zettlr.com) by providing a few options that help with file organization and creating an efficient workflow. '))
    text.append(textwrap.fill(f'Currently, the app has a few limitations: zettels must be of type ".md" and assets of types {asset_types_str}. Zettel links must be 14-digit numbers enclosed in double square brackets, and asset links must use markdown\'s link syntax. More options coming soon!'))
    text.append(textwrap.fill('Here\'s what the menu options do:'))
    text.append(textwrap.fill('Split zettels: splits zettels containing the tag "#split" each into multiple zettels based on a header level of your choice.'))
    text.append(textwrap.fill('Check media: searches the zettelkasten for unused assets, broken file links, and various anti-patterns.'))
    text.append(textwrap.fill('Move media: moves assets from one folder to another, and automatically updates their links in the zettelkasten.'))
    text.append(textwrap.fill('You can find more details in the app\'s README.'))
    return '\n\n'.join(text)


def get_about_text():
    text = []
    text.append(textwrap.fill('On Mend\'s GitHub page, you can find a more in-depth guide, submit a bug report or feature request, voice questions or concerns, and see all the source code for this app.'))
    return '\n\n'.join(text)


def get_license_text():
    text = []
    text.append(textwrap.fill('<License here>'))  # TODO: add license.
    return '\n\n'.join(text)


def respond_to_menu_event(event):
    if event == '-README-':
        # TODO: use Mend links instead of Zettlr links.
        webbrowser.open('https://github.com/Zettlr/Zettlr/blob/master/README.md', new=2)
    elif event == '-source-':
        webbrowser.open('https://github.com/Zettlr/Zettlr')
    elif event == '-issues-':
        webbrowser.open('https://github.com/Zettlr/Zettlr/issues', new=2)
    elif event == '-discuss-':
        webbrowser.open('https://github.com/Zettlr/Zettlr/projects', new=2)
