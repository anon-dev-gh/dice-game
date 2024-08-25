from typing import Optional

from di import Container, bind_by_type
from di.dependent import Dependent
from di.exceptions import WiringError
from di.executors import SyncExecutor

from dice_game.domain.add_player import AddPlayer
from dice_game.domain.assign_current_player import AssignCurrentPlayer


class SingletonContainer:
    # We can't make SingletonContainer(Singleton, Container)
    # because the Container constructor resets bind_hooks.
    _instance: Optional[Container] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Container()
        return cls._instance


def setup_container() -> Container:
    container = SingletonContainer.get_instance()
    # checking _bind_hooks is an ugly hack to bind only once
    if not container._bind_hooks:
        _bind(container, AddPlayer, AddPlayer)
        _bind(container, AssignCurrentPlayer, AssignCurrentPlayer)
    return container


def _bind(container, provider, dependency, scope=None):
    container.bind(bind_by_type(Dependent(provider, scope=scope), dependency))


def solve(service_type, scope=None):
    container = setup_container()
    with container.enter_scope(scope) as state:
        try:
            solved = container.solve(
                Dependent(service_type, scope=scope), scopes=[scope]
            )
            return solved.execute_sync(executor=SyncExecutor(), state=state)
        except WiringError:
            return None
