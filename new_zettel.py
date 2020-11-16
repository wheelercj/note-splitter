# Create a new zettel with auto-generated YAML frontmatter.

import pyautogui

# Find the Zettlr window(s).
windows = pyautogui.getWindowsWithTitle('Zettlr')
if len(windows) == 0:
    pyautogui.alert('Please open Zettlr and try again.')
else:
    # Read the new zettel's title from user.
    title = pyautogui.prompt('Title:')
    if title is not None and title != '':
        # Bring Zettlr to the front.
        windows[0].activate()
        pyautogui.sleep(0.15)

        # Create a new zettel.
        pyautogui.hotkey('ctrl', 'n')
        pyautogui.sleep(0.15)
        pyautogui.press('enter')
        pyautogui.sleep(0.35)

        # Insert the YAML frontmatter and the title.
        pyautogui.write('---')
        pyautogui.write('\ntitle: ' + title)
        pyautogui.write('\n---')
        pyautogui.hotkey('shift', '\n')
        pyautogui.write('\n# ' + title)
        pyautogui.write('\n#')
