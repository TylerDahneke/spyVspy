import tkinter as tk
import spy_agent
import spy_grid

# GLOBALS

BoardWidth = 600
BoardHeight = BoardWidth

TileInRow = 6
TileInCol = TileInRow

TotalTileWidth = BoardWidth // TileInRow
TotalTileHeight = BoardHeight // TileInCol

TileWidthPadding = .2 * TotalTileWidth
TileHeightPadding = .2 * TotalTileHeight

RawTileWidth = TotalTileWidth - 2 * TileWidthPadding
RawTileHeight = TotalTileHeight - 2 * TileHeightPadding

AgentWidth = .3 * RawTileWidth
AgentHeight = .3 * RawTileHeight

ColorList = ['blue', 'red', 'green', 'yellow', 'orange', 'purple']

InputGrid = '0.0. 100.0. 200.0. 300.0. 400.0. 500.0._0.100. 100.100. 200.100. 300.100. 400.100.blue.red. 500.100._0.200. ' \
            '100.200. 200.200. 300.200. 400.200. 500.200._0.300.red. 100.300. 200.300. 300.300. 400.300. ' \
            '500.300._0.400. 100.400. 200.400.green. 300.400. 400.400. 500.400._0.500. 100.500. 200.500. 300.500. 400.500. ' \
            '500.500._ '


# END GLOBALS

def create_grid_from_str(canvas, inp_str):
    outer_shell = []
    inner_shell = []
    while True:
        if inp_str == ' ':
            outer_shell.append(inner_shell)
            break
        x_pos, inp_str = int(inp_str[:inp_str.find('.')]), inp_str[inp_str.find('.') + 1:]
        y_pos, inp_str = int(inp_str[:inp_str.find('.')]), inp_str[inp_str.find('.') + 1:]
        new_tile = spy_grid.Tile(canvas, (x_pos, y_pos))
        inner_shell.append(new_tile)
        if inp_str[0].isalpha():
            while inp_str[0].isalpha():
                agent_color, inp_str = inp_str[:inp_str.find('.')], inp_str[inp_str.find('.') + 1:]
                new_agent = spy_agent.agent(canvas, agent_color)
                new_tile.add_agent(new_agent)
        if inp_str[0] == ' ':
            inp_str = inp_str[1:]
        elif inp_str[0] == '_':
            outer_shell.append(inner_shell)
            inner_shell = []
            inp_str = inp_str[1:]
    return spy_grid.Grid(canvas, contents=outer_shell)


class display:

    def __init__(self, master=None):
        self.master = master
        self.canvas = tk.Canvas(master, width=BoardWidth, height=BoardHeight)

        self.grid_adt = create_grid_from_str(self.canvas, InputGrid)

        self.canvas.pack()

    def display_all_agents(self):
        self.grid_adt.display_all_agents()

    def hide_all_agents(self):
        self.grid_adt.hide_all_agents()


def main():
    root = tk.Tk()
    base = display(root)

    root.bind('<KeyPress-d>', lambda _: base.display_all_agents())
    root.bind('<KeyPress-h>', lambda _: base.hide_all_agents())

    tk.mainloop()


if __name__ == '__main__':
    main()
