from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal


Maybe = Literal[
    False,  # Doesn't exist
    True,   # Must exist
    'maybe' # Might exist
]


@dataclass(frozen=True, kw_only=True)
class JoinRule:
    affix: Maybe
    word: Maybe
    required: bool

    def affix_required(self, have_word: bool) -> bool:
        return (self.affix is True) or (self.required and not have_word)
    
    @property
    def affix_allowed(self) -> bool:
        return self.affix is not False
    
    def word_required(self, have_affix: bool) -> bool:
        return (self.word is True) or (self.required and not have_affix)
    
    @property
    def word_allowed(self) -> bool:
        return self.word is not False


@dataclass(frozen=True)
class Part:
    string: str
    after: JoinRule


type Weighted[T] = tuple[T, float]
type MaybeWeighted[T] = T | Weighted[T]


def get_option_and_weight[T](option: MaybeWeighted[T]) -> Weighted[T]:
    if isinstance(option, tuple) and len(option) == 2 and isinstance(option[1], (int, float)):
        return option
    else:
        return option, 1


def get_options_and_weights[T](options: Sequence[MaybeWeighted[T]]) -> tuple[list[T], list[float]]:
    return list(zip(*(get_option_and_weight(option) for option in options)))


# Each element is a list of mutually exclusive options for a join.
# Joins must occur in the overall name in the order given here.
JoinOptions = tuple[MaybeWeighted[tuple[MaybeWeighted[str], ...]], ...]
