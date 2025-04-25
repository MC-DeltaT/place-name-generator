from typing import Literal

from placenamegen.common import JoinRule, Part


JoinRuleStr = Literal[
    '',     # Can't join
    'a',    # Affix optional
    'a!',   # Affix required
    'w',    # Word optional
    'w!',   # Word required
    'aw',   # Affix optional, word optional
    'a!w',  # Affix required, word optional
    'aw!',  # Affix optional, word required
    'a!w!', # Affix required, word required
    '!'     # Word or affix, at least one is required
]


def join_rule_from_str(s: JoinRuleStr) -> JoinRule:
    required = s == '!'
    if required:
        affix = 'maybe'
        word = 'maybe'
    else:
        if 'a!' in s:
            affix = True
        elif 'a' in s:
            affix = 'maybe'
        else:
            affix = False
        if 'w!' in s:
            word = True
        elif 'w' in s:
            word = 'maybe'
        else:
            word = False
    return JoinRule(
        affix=affix,
        word=word,
        required=required
    )


def base_part(string: str, suffix: JoinRuleStr) -> Part:
    return Part(string, join_rule_from_str(suffix))


def base_word(string: str, *, s: JoinRuleStr = 'aw') -> Part:
    """Base part that doesn't require affixes or before/after words."""

    return base_part(string, s)


def base_head(string: str, *, s: JoinRuleStr = '!') -> Part:
    """Base part that requires a suffix or after word."""

    return base_part(string, s)


def base_prefix(string: str, *, s: JoinRuleStr = 'a!') -> Part:
    """Base part that needs a suffix."""

    return base_part(string, s)
