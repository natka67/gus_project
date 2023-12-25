from gui import Gui

if __name__ == "__main__":
    try:
        gui = Gui()
        gui.start_program() # start_program()
    except Exception as err:
        Gui().create_message_window(message=f"{str(type(err)).capitalize()}: {err}")
        print(type(err), err)
