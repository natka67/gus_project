from gui import Gui

if __name__ == "__main__":
    gui = Gui()
    try:
        gui.start_program()  # start_program()
    except Exception as err:
        gui.create_message_window(message=f"{str(type(err)).capitalize()}: {err}")
