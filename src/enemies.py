from sprite_sheet import EnemySheet
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        x_coord: int,
        y_coord: int,
        width: int,
        height: int,
        enemies_sheet: EnemySheet,
        *groups,
    ):
        super().__init__(*groups)

        self.x_coord = x_coord
        self.y_coord = y_coord

        # Calculate position
        # -> * tile width
        self.x_pos = self.x_coord * 50
        self.y_pos = self.y_coord * 50

        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

        self.render(enemies_sheet)

    def render(self, enemies_sheet: EnemySheet):
        self.image.blit(enemies_sheet.enemy_1, (0, 0))

    def navigate(self, map_data):
        class Node:
            def __init__(self, parent, position):
                self.parent = parent
                self.position = position

                self.g_cost = 0
                self.h_cost = 0
                self.t_cost = 0

        surrounding_nodes = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        opened = []
        closed = []

        start = Node(None, (self.x_coord, self.y_coord))
        end = Node(None, (3, 3))

        opened.append(start)

        # Loop
        run = True
        while run:
            
            # Start current
            current = opened[0]
            current_index = 0
            for index, node in enumerate(opened):
                if node.t_cost < current.t_cost:
                    current = node
                    current_index = index

            # Move current to closed
            opened.pop(current_index)
            closed.append(current)

            # If finished
            if current.position == end.position:

                path = []
                node = current
                while node is not None:
                    path.append(node.position)
                    node = node.parent

                run = False
                return path

            # Create node children
            children = []
            for new_pos in surrounding_nodes:

                neighbour_pos = (
                    (current.position[0] + new_pos[0]),
                    (current.position[1] + new_pos[1]),
                )

                # If the area isn't walkable, skip
                if map_data[f"{neighbour_pos[0]},{neighbour_pos[1]}"][0] not in (
                    "Buildable_1",
                    "Buildable_0",
                ):
                    continue

                new_node = Node(current, neighbour_pos)
                children.append(new_node)

            for child in children:

                for closed_child in closed:
                    if child == closed_child:
                        continue

                child.g_cost = current.g_cost + 1
                child.h_cost = ((child.position[0] - end.position[0]) ** 2) + (
                    (child.position[1] - end.position[1]) ** 2
                )
                child.t_cost = child.g_cost + child.h_cost

                # Child is already in the open list
                for open_node in opened:
                    if child == open_node and child.g_cost > open_node.g_cost:
                        continue

                # Add the child to the open list
                opened.append(child)

    def update(self):

        pass
