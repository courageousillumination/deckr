from engine.core.decorators import game_action
from engine.core.game import Game
from engine.core.game_object import GameObject


class FooObject(GameObject):

    def __init__(self):
        super(FooObject, self).__init__()

        self.foo = 'foo'
        self.game_object_type = 'FooObject'
        self.game_attributes.add('foo')


class TestGame(Game):

    def set_up(self):
        self.foo_object = FooObject()
        self.register(self.foo_object)
        self.foo_object.foo = 'bar'
        self.foo_object.set_player_override('foo', 'baz', self.players[0])

    def is_over(self):
        return False

    def winners(self):
        return []

    @game_action(parameter_types=None, restriction=None)
    def change_foo(self, player, new_foo_value):
        self.foo_object.set_player_override('foo', new_foo_value, player)
