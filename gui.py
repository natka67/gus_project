import tkinter as tk
class Gui:
    functionalities = sorted(
        ['Create Visual', 'Create Ranking', 'Check Correlation', 'Compare Areas', 'Download Dataset'])

    def button_click(self,option, window):
        pass
    def start_program(self):
        window = tk.Tk()
        # Displaying window at the center of a screen
        height = 225
        width = 450
        window.geometry(f"{width}x{height}")
        center_x = int((window.winfo_screenwidth() - width) / 2)
        center_y = int((window.winfo_screenheight() - height) / 2)
        window.geometry(f"+{center_x}+{center_y}")

        # Adding buttons for every available function
        for function in self.functionalities:
            button = tk.Button(window, text=function, command=lambda option=function: self.button_click(option, window))
            button.pack(pady=5)
        window.mainloop()


if __name__ == "__main__":
    try:
        gui = Gui()
        gui.start_program()
    except Exception as err:
        print(type(err), err)