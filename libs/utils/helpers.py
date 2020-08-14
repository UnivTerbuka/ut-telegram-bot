
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        if type(header_buttons) == list:
            menu.insert(0, header_buttons)
        else:
            menu.insert(0, [header_buttons])
    if footer_buttons:
        if type(footer_buttons) == list:
            menu.append(footer_buttons)
        else:
            menu.append([footer_buttons])
    return menu
