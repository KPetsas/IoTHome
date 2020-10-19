from abc import ABC, abstractmethod


class Router(ABC):
    """
    Abstract class for all the router classes defined in routes.py files (convention).
    """

    def __init__(self, api):
        """ Constructor ensures to register all routes. """
        self.register_routes(api)

    @abstractmethod
    def register_routes(self):
        """ Abstract method to relate endpoints with controllers. """
        raise NotImplementedError()
