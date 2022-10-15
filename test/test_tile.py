from tile import Direction


def test_direction():
    assert Direction.opposite(Direction.N) == Direction.S
    assert Direction.opposite(Direction.E) == Direction.W
    assert Direction.opposite(Direction.S) == Direction.N
    assert Direction.opposite(Direction.W) == Direction.E