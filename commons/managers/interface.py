from abc import ABC, abstractmethod


class AbstractManageService(ABC):

    @abstractmethod
    async def to_execute(*args, **kwargs):
        ...
