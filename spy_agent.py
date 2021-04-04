import random

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

agent_id = -1

ColorList = ['blue', 'red', 'green', 'yellow', 'orange', 'purple']


# END GLOBALS

def get_id():
    global agent_id
    agent_id += 1
    return agent_id



class agent:

    def __init__(self, canvas, color=None):
        self.canvas = canvas
        self.canvas_shape = None
        if color is None:
            self.color = 'blue'
        else:
            self.color = color
        self.id = get_id()

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def draw(self, x, y):
        x -= AgentWidth // 2
        y -= AgentHeight // 2
        self.canvas_shape = self.canvas.create_oval(x, y, x + AgentWidth, y + AgentHeight,
                                                    fill=self.color)

    def delete_shape(self):
        self.canvas.delete(self.canvas_shape)
        self.canvas_shape = None
