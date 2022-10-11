from tkinter import *
import tkinter.colorchooser
from PIL import ImageGrab
from datetime import datetime


class PixelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art")

        cell_length = 50
        grid_width = 20
        grid_height = 10

        self.color_chooser = tkinter.colorchooser.Chooser(self.root)
        self.chosen_colour = None
        self.is_pencil_selected = False
        self.is_eraser_selected = False

        #-------------------ALL THE CANVAS------------#

        self.drawing_grid = Canvas(self.root)
        self.drawing_grid.grid(column=0, row=0, sticky=(N, E, S, W))

        self.cells = []
        for i in range(0, grid_height):
            for j in range(0, grid_width):
                cell = Frame(self.drawing_grid, width=cell_length, height=cell_length, bg="white",
                             highlightbackground="black", highlightcolor="black", highlightthickness=1)
                cell.grid(column=j, row=i)
                cell.bind('<Button-1>', self.tap_cell)
                self.cells.append(cell)

        #------------------ROW FOR THE BUTTONS----------------#

        control_frame = Frame(self.root, height= cell_length)
        control_frame.grid(column=0, row=1, sticky=(N, E, S, W))

        new_button = Button(control_frame, text="New", command=self.press_new_button)
        new_button.grid(column=0, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        save_button = Button(control_frame,text="Save", command=self.press_save_button)
        save_button.grid(column=2, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        self.pencil_image = PhotoImage(file='Course_Files/pencil.png').subsample(2, 3)
        pencil_button = Button(control_frame, text="Pencil", image=self.pencil_image, command=self.press_pencil_button)
        pencil_button.grid(column=8, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        self.eraser_image = PhotoImage(file='Course_Files/eraser.png').subsample(2, 3)
        erase_button = Button(control_frame, text="Erase", image=self.eraser_image, command=self.press_erase_button)
        erase_button.grid(column=10, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)

        self.selected_colour_box = Frame(control_frame, borderwidth=2, relief="raise", bg="white")
        self.selected_colour_box.grid(column=15, row=0, sticky=(N, E, S, W), padx=7, pady=7)

        pick_colour_button = Button(control_frame, text="Pick colour", command=self.press_pick_colour_button)
        pick_colour_button.grid(column=17, row=0, columnspan=3, sticky=(N, E, S, W), padx=5, pady=5)

        cols, rows = control_frame.grid_size()
        for col in range(cols):
            control_frame.columnconfigure(col, minsize=cell_length)
        control_frame.rowconfigure(0, minsize=cell_length)


    #---------- Functions------------#

    def tap_cell(self, event):
        widget = event.widget
        index = self.cells.index(widget)
        selected_cell = self.cells[index]
        if self.is_eraser_selected:
            selected_cell["bg"] = "white"
        if self.is_pencil_selected and self.chosen_colour != None:
            selected_cell["bg"] = self.chosen_colour

    def press_new_button(self):
        for cell in self.cells:
            cell["bg"] = "white"
        self.selected_colour_box["bg"] = "white"
        self.chosen_colour = None
        self.is_pencil_selected = False
        self.is_eraser_selected = False


    def press_save_button(self):
        x = self.root.winfo_rootx() + self.drawing_grid.winfo_x()
        y = self.root.winfo_rootx() + self.drawing_grid.winfo_y() + 35

        width = x + 1000
        height = y + 487

        image_name =  datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".png"
        _ = ImageGrab.grab(bbox=(x, y, width, height)).save(image_name)

    def press_pencil_button(self):
        self.is_pencil_selected = True
        self.is_eraser_selected = False

    def press_erase_button(self):
        self.is_pencil_selected = False
        self.is_eraser_selected = True

    def press_pick_colour_button(self):
        colour_info = self.color_chooser.show()

        chosen = colour_info[1]
        if chosen != None:
            self.chosen_colour = chosen
            self.selected_colour_box["bg"] = self.chosen_colour




root = Tk()
PixelApp(root)
root.mainloop()
