from collections import defaultdict
from typing import Any, List, Set, Tuple, DefaultDict, Callable, AnyStr
from typing import TypeVar, Union, Iterable, Iterator, NoReturn

State = TypeVar("State")
States = Set[State]

InitState = State
NextState = Union[None, State]
TransitionFunctionOutcome = Union[None, Any]
TransitionResult = bool
TransitionFunctionResult = Tuple[NextState, TransitionFunctionOutcome, TransitionResult]
TransitionFunction = Callable[[Any], TransitionFunctionResult]


def default_field(obj: Any) -> Any:
    return field(default_factory=lambda: obj)


@dataclass
class DFA(object):
    states: States
    accept_states: States
    transition_table: DefaultDict[AnyStr, List[TransitionFunction]] = default_field(defaultdict(list))
    current_state: State = None

    def add_transition_function(self, last_states: States, func: TransitionFunction) -> NoReturn:
        for s in last_states:
            self.transition_table[str(s)].append(func)

    class End(Exception):
        pass

    class BadThing(Exception):
        pass

    def start(self, init_state: InitState, flow: Iterable[Any]) -> Iterator[Any]:
        self.current_state = init_state
        for thing in flow:
            if self.current_state in self.accept_states:
                raise DFA.End()
            last_state = self.current_state
            for func in self.transition_table.get(str(last_state), []):
                next_state, result, eat_it = func(thing)
                if not eat_it:
                    continue
                self.current_state = next_state
                yield result
                break
            if self.current_state == last_state:
                raise DFA.BadThing(thing)

