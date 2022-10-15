import enum
import typing
import random

from tile import Tile, Direction
from tile_pool import TilePool


class InvalidLayoutError(Exception):
    pass


class QuantumTile:
    def __init__(self, pool: TilePool):
        self.tile_pool = pool
        self._edges = self.initialize()
        self.neighbors: typing.List[typing.Optional[QuantumTile]] = [None] * 4

    def initialize(self):
        self._edges = [{0, 1} for _ in Direction]
        return self._edges

    @property
    def edges(self):
        return tuple(tuple(edge) for edge in self._edges)

    @property
    def assigned(self):
        return all(len(e) == 1 for e in self._edges)

    @property
    def valid_tile_count(self):
        return len(self.tile_pool.get_valid_tiles(self.edges))

    def set_neighbor(self, direction, neighbor: 'QuantumTile'):
        self.neighbors[direction] = neighbor
        opposite_direction = direction - 2
        neighbor.neighbors[opposite_direction] = self

    def set_random(self):
        tile = self.tile_pool.get_random(self.edges)
        return self.set_tile(tile)

    def set_tile(self, tile: Tile) -> set['QuantumTile']:
        dirty = set()
        for d in Direction:
            if self.neighbors[d] and self._edges[d] != {tile.edges[d]}:
                dirty.add(self.neighbors[d])
            self._edges[d] = {tile.edges[d]}
        return dirty

    def get_dirty_neighbors(self) -> list['QuantumTile']:
        dirty_neighbors = []
        for d in Direction:
            neighbor = self.neighbors[d]
            if neighbor is None:
                continue
            if not self.neighbors[d].edges[d - 2] == self.edges[d]:
                dirty_neighbors.append(self.neighbors[d])
        return dirty_neighbors

    def update_edges(self):
        for d in Direction:
            neighbor = self.neighbors[d]
            if neighbor is None:
                continue
            neighbor_edge = neighbor.edges[d - 2]
            # print(f'dir: {d}, {neighbor.edges}')
            self._edges[d] = self._edges[d].intersection(neighbor_edge)
        self._filter_edges()

    def _filter_edges(self):
        filtered_edges = self.tile_pool.get_valid_edges(self.edges)
        # print(f'filtered edges (pool): {filtered_edges}')
        for d in Direction:
            self._edges[d] = self._edges[d].intersection(filtered_edges[d])
        if any(len(e) == 0 for e in self._edges):
            raise InvalidLayoutError

    def __repr__(self):
        return f'<QuantumTile {self.valid_tile_count}>'

    # def update_edge(self, direction, new_edges):
    #     if self.edges[direction] == new_edges:
    #         return
    #     old_edges = self.edges
    #     edge_pool = list(self.edges)
    #     edge_pool[direction] = new_edges
    #     self.edges = tuple(edge_pool)
    #     self.update_pool()
    #     for direction, old, new in zip(range(4), old_edges, self.edges):
    #         if not old == new:
    #             self.update_neighbor(direction)
