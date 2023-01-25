from note_splitter import gui


def test_create_hyperlink():
    display_text = "zombo com"
    url = "https://zombo.com/"
    sg_text_object = gui.create_hyperlink(display_text, url)
    assert sg_text_object.DisplayText == display_text
    assert sg_text_object.Tooltip == url
