import tkinter as tk
import tkinter.messagebox
import customtkinter
import os



customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def get_canvas_bg_color():
    appearance_mode = customtkinter.get_appearance_mode()
    if appearance_mode == "Light":
        return "gray81"  # or any other light color
    elif appearance_mode == "Dark":
        return "gray20"  # or any other dark color
    else:
        return "gray81"  # default color

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Partition Manager GUI")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Partitions", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        
        self.directory = os.path.join(os.getcwd(), "partitions")
        
        self.buttons_container = customtkinter.CTkFrame(self.sidebar_frame)
        self.buttons_container.grid(row=1, column=0, sticky='nsew', padx=(20, 0), pady=(0, 10))
        self.sidebar_frame.grid_rowconfigure(1, weight=1)  # Allow this row to expand

        # Create a canvas within the container, and a scrollbar linked to this canvas
        self.canvas_color = self.buttons_container.cget('fg_color')  # Assume fg_color is used for the theme
        self.canvas = tk.Canvas(self.buttons_container, bg="grey17", highlightthickness=0, width = 6)
        self.scrollbar = customtkinter.CTkScrollbar(self.buttons_container,bg_color="grey17", command=self.canvas.yview, width=10)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid the canvas and the scrollbar in the container
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.buttons_container.grid_columnconfigure(0, weight=1)
        self.buttons_container.grid_rowconfigure(0, weight=1)

        # Create a frame within the canvas for the buttons
        self.scrollable_frame = customtkinter.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        # Bind the update of the scroll region to the size of the scrollable frame
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        try:
            row = 0
            files = os.listdir(self.directory)
            for file in files:
                if not file.endswith(".cfg"):
                    button = customtkinter.CTkButton(self.scrollable_frame, text=file, command=lambda f=file: self.file_button_event(f))
                    button.grid(row=row, column=0, pady=5, sticky='ew')
                    row += 1
        except FileNotFoundError:
            print(f"Directory not found: {self.directory}")

        self.search_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Search Partitions")
        self.search_entry.grid(row=2, column=0, padx=20, pady=(10, 10))
            
        

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")




        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")


        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

      

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def update_canvas_bg(self):
        new_color = get_canvas_bg_color()
        if new_color == "gray20":
            new_color = "gray17"
        else:
            new_color = "gray85"
        self.scrollbar.configure(bg_color=new_color)
        self.canvas.configure(bg=new_color)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.update_canvas_bg()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()