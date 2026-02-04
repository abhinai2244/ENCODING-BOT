from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class ButtonMaker:
    def __init__(self):
        self._buttons = []
        self._header_buttons = []
        self._footer_buttons = []

    def button_data(self, text, data, position=None):
        button = InlineKeyboardButton(text=text, callback_data=data)
        if position == 'header':
            self._header_buttons.append(button)
        elif position == 'footer':
            self._footer_buttons.append(button)
        else:
            self._buttons.append(button)

    def button_url(self, text, url, position=None):
        button = InlineKeyboardButton(text=text, url=url)
        if position == 'header':
            self._header_buttons.append(button)
        elif position == 'footer':
            self._footer_buttons.append(button)
        else:
            self._buttons.append(button)

    def build_menu(self, n_cols):
        menu = [self._buttons[i:i + n_cols] for i in range(0, len(self._buttons), n_cols)]
        if self._header_buttons:
            menu.insert(0, self._header_buttons)
        if self._footer_buttons:
            menu.append(self._footer_buttons)
        return InlineKeyboardMarkup(menu)
