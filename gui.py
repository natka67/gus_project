import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import etl
import comparison
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class Gui:
    functionalities = sorted(
        ['Create Visual', 'Create Ranking', 'Check Correlation', 'Compare Areas', 'Download Dataset'])

    def __init__(self):
        self.graph = None
        self.voivodeships_poland = dict(pd.read_excel('voivodeships_poland.xlsx', dtype={'id': str})[['id', 'name']].values).values()

    def button_click(self,option, window):
        match option:
            case 'Download Dataset':
                etl.get_dataset(self.voivodeships_poland).to_excel('gus.xlsx')
                self.create_success_window()
            case 'Compare Areas':
                window.destroy()
                comparison.start_functionality()
            case 'Create Visual':
                window.destroy()
                self.create_window_for_visuals()
            case _: print("else...")
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
        window.title("Menu")
        # Adding buttons for every available function
        for function in self.functionalities:
            button = tk.Button(window, text=function, command=lambda option=function: self.button_click(option, window))
            button.pack(pady=5)
        window.mainloop()

    def create_success_window(self):
        root = tk.Tk()
        root.geometry("200x100")
        root.title("Success")
        success_label = tk.Label(root, text="Download Succeeded")
        success_label.pack(expand=True)
        root.mainloop()

    def create_window_for_visuals(self):
        root = tk.Tk()
        root.title('Visualisation')
        #root.create_widgets()
        height = 1000
        width = 1720
        root.geometry(f"{width}x{height}")
        center_x = int((root.winfo_screenwidth() - width) / 2)
        center_y = int((root.winfo_screenheight() - height) / 2)
        root.geometry(f"+{center_x}+{center_y}")

        col_names = list(pd.read_excel('details_variabled.xlsx')['name'])

        def update_ui(*args):
            selected_value = dropdown1.get()
            if selected_value == "Scatter Plot":
                dropdown3.grid()
            else:
                dropdown3.grid_remove()

        # Left frame for dropdowns and buttons
        left_frame = ttk.Frame(root, padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Dropdowns and Buttons
        ttk.Label(left_frame, text="Type:").grid(row=0, column=0, pady=5, sticky=tk.W)
        dropdown1_var = tk.StringVar()
        dropdown1 = ttk.Combobox(left_frame, values=['Map', 'Scatter Plot'], state="readonly", textvariable=dropdown1_var, width=40)
        dropdown1.grid(row=0, column=1, pady=5, padx=(0, 10))
        dropdown1_var.trace_add("write", update_ui)

        ttk.Label(left_frame, text="Column:").grid(row=1, column=0, pady=5, sticky=tk.W)
        dropdown2 = ttk.Combobox(left_frame, values=col_names, state="readonly", width=40)
        dropdown2.grid(row=1, column=1, pady=5, padx=(0, 10))

        dropdown3 = ttk.Combobox(left_frame, values=col_names, state="readonly", width=40)
        dropdown3.grid(row=2, column=1, pady=5, padx=(0, 10))

        def generate_plot():
            type_value = dropdown1.get()
            column1_value = dropdown2.get()
            column2_value = dropdown3.get()

        def return_to_menu():
            root.destroy()
            self.start_program()

        def save_as_pdf():
            pass

        ttk.Button(left_frame, text="Generate Plot", command=generate_plot).grid(row=3, column=0, columnspan=1, pady=10)

        ttk.Button(left_frame, text="Navigation", command=return_to_menu).grid(row=3, column=1, columnspan=1, pady=10)

        ttk.Button(left_frame, text="Download", command=save_as_pdf).grid(row=3, column=2, columnspan=1, pady=10)

        # Right frame for the plot
        right_frame = ttk.Frame(root)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Matplotlib plot
        figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, master=right_frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Resize weight for frames
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=2)
        root.grid_columnconfigure(1, weight=8)

        root.mainloop()

if __name__ == "__main__":
    try:
        gui = Gui()
        gui.start_program()
    except Exception as err:
        print(type(err), err)