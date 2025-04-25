from collections.abc import Sequence
from dataclasses import dataclass

from placenamegen.common import JoinOptions, MaybeWeighted, Part


Bases = Sequence[MaybeWeighted[Part]]
BeforeWords = JoinOptions
AfterAffixes = JoinOptions
AfterWords = JoinOptions


@dataclass(frozen=True)
class Config:
    bases: Bases
    before_words: BeforeWords
    after_affixes: AfterAffixes
    after_words: AfterWords
    before_word_probability: float
    after_affix_probability: float
    after_word_probability: float
