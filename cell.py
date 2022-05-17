from tkinter import Button, Label
import random
import settings

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.isShown = False


        # Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4#,
            #text=f'{self.x},{self.y}'
        )
        btn.bind('<Button-1>', self.left_click_actions) #left click
        btn.bind('<Button-3>', self.right_click_actions)  # right click

        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg=settings.BLACK,
            fg = settings.WHITE,
            width=12,
            height=4,
            text=f'Cell Left:{Cell.cell_count}',
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl


    def left_click_actions(self, event):
        def show_near_cells(cl):
            for cell_obj in cl.surrounded_cells:
                if cell_obj.surrounded_cells_mines_length == 0 and not cell_obj.isShown:
                    cell_obj.isShown = True
                    show_near_cells(cell_obj)
                cell_obj.show_cell()



        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()
            if self.surrounded_cells_mines_length == 0:
                show_near_cells(self)


    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the value of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1),
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        return sum(bool(cell.is_mine) for cell in self.surrounded_cells)


    def show_cell(self):
        if not self.isShown:
            Cell.cell_count-=1
        self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
        self.isShown = True
        # Replace the text of cell count label with the newer count
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(
                text=f'Cell Left:{Cell.cell_count}'
            )






    def show_mine(self):
        # A logic do interrupt the game and display a message that player lost!
        self.cell_btn_object.configure(bg=settings.RED)
        self.isShown = True


    def right_click_actions(self, event):
        print(event)
        print("I am right clicked!")

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"