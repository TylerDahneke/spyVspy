import spy_agent
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

ColorList = ['blue', 'red', 'green', 'yellow', 'orange', 'purple']


# END GLOBALS





class Tile:

    def __init__(self, canvas, pos, server=False):
        self.canvas = canvas
        self.x, self.y = self.pos = pos
        self.agent_list = []
        self.num_agents = 0
        if server is False:
            self.canvas_shape = self.draw_base_tile()
        else:
            self.canvas_shape = None

    def __repr__(self):
        return f'{self.pos}, {self.agent_list}'

    def get_pos(self):
        return self.pos

    def draw_agents(self):
        if not self.num_agents:
            pass
        if self.num_agents == 1:
            self.agent_list[0].draw(self.x + (TotalTileWidth // 2), self.y + (TotalTileHeight // 2))
        elif self.num_agents == 2:
            self.agent_list[0].draw(self.x + (TotalTileWidth // 2) - AgentWidth,
                                    self.y + (TotalTileHeight // 2))
            self.agent_list[1].draw(self.x + (TotalTileWidth // 2) + AgentWidth,
                                    self.y + (TotalTileHeight // 2))

    def erase_agents(self):
        for agent in self.agent_list:
            agent.delete_shape()

    def draw_base_tile(self):
        return self.canvas.create_rectangle(self.x + TileWidthPadding, self.y + TileHeightPadding,
                                            self.x + TileWidthPadding + RawTileWidth,
                                            self.y + TileHeightPadding + RawTileHeight)

    def add_agent(self, agent):
        self.agent_list.append(agent)
        self.num_agents += 1

    def pop_agent_by_id(self, agent_id):
        counter = 0
        r_agent = None
        for agent in self.agent_list:
            if agent.id == agent_id:
                r_agent = self.agent_list.pop(counter)
                self.num_agents -= 1
        if r_agent is None:
            return False
        else:
            return r_agent

    def export_to_str(self):
        r_str = ''
        r_str += f'{self.x}.{self.y}.'
        for agent in self.agent_list:
            r_str += f'{agent.color}.{agent.id}.'
        r_str += ' '
        return r_str


class Grid:

    def __init__(self, canvas, contents=None, server=False):
        self.canvas = canvas
        self.server = server
        if contents is None:
            self.contents = self.get_contents()
        else:
            self.contents = contents

    def __repr__(self):
        return self.contents

    def get_contents(self):
        outer_shell = []
        for col_index in range(TileInCol):
            inner_shell = []
            for row_index in range(TileInRow):
                new_tile_pos = (row_index * TotalTileWidth, col_index * TotalTileHeight)
                new_tile = Tile(self.canvas, new_tile_pos, self.server)
                inner_shell.append(new_tile)
            outer_shell.append(inner_shell)
        return outer_shell

    def display_all_agents(self):
        for col_index in range(TileInCol):
            for row_index in range(TileInRow):
                curr_tile = self.get_tile_from_pos(row_index, col_index)
                curr_tile.draw_agents()

    def hide_all_agents(self):
        for col_index in range(TileInCol):
            for row_index in range(TileInRow):
                curr_tile = self.get_tile_from_pos(row_index, col_index)
                curr_tile.erase_agents()

    def get_tile_from_pos(self, x, y):
        return self.contents[y][x]

    def add_agent(self, agent=None, pos=None):
        if pos is None:
            x, y = random.randint(0, TileInRow - 1), random.randint(0, TileInCol - 1)
        else:
            x, y = pos
        if agent is None:
            agent = spy_agent.agent(self.canvas, color=random.choice(ColorList))
        else:
            agent = agent
        self.get_tile_from_pos(x, y).add_agent(agent)

    def move_agent(self, agent_id, curr_pos, new_pos):
        old_x, old_y = curr_pos
        new_x, new_y = new_pos

        old_tile = self.get_tile_from_pos(old_x, old_y)
        new_tile = self.get_tile_from_pos(new_x, new_y)

        ph_agent = old_tile.pop_agent_by_id(agent_id)
        new_tile.add_agent(ph_agent)

    def export_to_str(self):
        r_str = ''
        for col_index in range(len(self.contents)):
            for row_index in range(len(self.contents[col_index])):
                curr_tile = self.get_tile_from_pos(row_index, col_index)
                r_str += curr_tile.export_to_str()
            r_str = r_str[:-1] + '_'
        return r_str
