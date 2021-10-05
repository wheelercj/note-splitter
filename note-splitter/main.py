# internal imports
from note import get_chosen_notes


def main():
    settings = get_settings()
    notes = get_chosen_notes(settings)


def get_settings() -> dict:
    """Gets the user's settings from settings.json."""
    # TODO


if __name__ == '__main__':
    main()
