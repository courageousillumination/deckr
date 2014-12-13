"""
This file provides all of the decorators for the engine. Most of these have
to do with game steps and actions.
"""

from engine.core.exceptions import InvalidMoveException, NeedsMoreInfo


def game_action(restriction = None, parameter_types = None):
    """
    This is a decorator that can be put around "actions" in Game. actions are
    defined as anything that the user can do. This could include playing a card,
    choosing a target, surrendering, etc.

    Each action comes with two optional parameters:
        1. restriction is a test that takes the same arguments as the function
           and returns either True or False. If it returns False then we raise
           an InvalidMoveException; otherwise we execute the function. This can
           be used to make sure that the user can only make specific actions
           at specific times.
        2. parameter_types is a list of dictionaries, specifying the parameters
           that are expected to this action and their types. This is to bridge
           the gap between the outside only using game_ids and the game class
           wanting to only work with GameObjects. Each element of
           parameter_types should be a dict with the following keys:
               * name: Name of the parameter
               * type (optional but encouraged): An expected class for this
                 parameter.
               * container (optional): If the parameter should be a 'list' of
                 values you can specify that here. Otherwise it is treated
                 as a singleton.
    """

    def wrapper(func):
        def inner(self, *args, **kwargs):
            # Fix up the parameter types
            if parameter_types is not None:
                for param in parameter_types:
                    obj = self.get_object_with_id(int(kwargs[param['name']]),
                                                  param.get('type', None))
                    if obj is None:
                        raise InvalidMoveException("Got bad parameter")
                    kwargs[param['name']] = obj

            # Check the actual restriction
            if restriction is None or restriction(self, *args, **kwargs):
                return func(self, *args, **kwargs)
            else:
                raise InvalidMoveException("Failed to pass restriction")
        return inner
    return wrapper

def game_step(requires=None):
    """
    A game step represents an atomic set of state transitions it the game.
    Each step can require specifc arguments; if these are not provided then
    an exception will be raised and the clients will be notified. Each
    requirement should be a dictionary with the following keys

        * name: The name of the required parameter.
        * type: A class specification of the required parameter type
        * container (optional): If the required parameter should come in a
          'list' mark that here.
        * prompt (optional): This string will be sent to the end user to give
          them a sense of what is required.
        * test (optional): If there is some requirement for this parameter
          that should be included here. This must take the same parameters as
          the step itself (usually you can get away with *args, and **kwargs)
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            if requires is not None:
                for requirement in requires:
                    expected_type = requirement['type']
                    name = requirement['name']
                    container = requirement.get('container', None)
                    test = requirement.get('test', None)

                    # Make sure the argument is present
                    if name not in kwargs:
                        raise NeedsMoreInfo('Missing required argument',
                                            requirement)

                    # Check the type
                    if container == 'list':
                        for x in kwargs[name]:
                            if not isinstance(x, expeted_type):
                                raise NeedsMoreInfo('Argument is improper type',
                                                    requirement)
                    elif not isinstance(kwargs[name], expected_type):
                        raise NeedsMoreInfo('Argument is improper type',
                                            requirment)

                    # Finally try the test
                    if test is not None and not test(*args, **kwargs):
                        raise NeedsMoreInfo('Failed Test',
                                            requirement)

            return func(*args, **kwargs)
        return inner
    return wrapper

def game_serialize(func):
    """
    This will take the return value of the wrapped function and do it's
    very best to replace all game objects with their IDs. This should be put
    on every function that interacts with the outside world.
    """

    def inner(*args, **kwargs):
        # Check for the serialize keyword
        serialize = kwargs.get('serialize', None)
        if serialize is not None:
            del kwargs['serialize']
        result = func(*args, **kwargs)
        if serialize:
            pass
        return result
    return inner
