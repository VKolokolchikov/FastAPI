import types
from abc import ABC


class AbstractService(ABC):
    manager = None
    model = None
    pk = None

    def __new__(cls, *args, **kwargs):
        mcls = super().__new__(cls, *args, **kwargs)

        for attr in cls.__dict__.values():
            if callable(attr) and isinstance(attr, types.FunctionType):
                if not attr.__annotations__.keys():
                    raise Exception(
                        f'You should use annotation for {cls.__name__}'
                    )

                try:
                    attr.__annotations__['session']
                except KeyError as _:
                    raise Exception(
                        f'You should add "session" in method {attr.__name__} from {cls.__name__}'
                    )

        return mcls

    def __init__(self, *args, **kwargs):
        assert self.manager is not None, 'Manager must not be None'
        assert self.model is not None, 'Model must not be None'
        super(AbstractService, self).__init__(*args, **kwargs)
