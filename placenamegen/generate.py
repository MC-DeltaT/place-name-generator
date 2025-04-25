from collections.abc import Iterable
from math import exp
from random import Random

from placenamegen.common import JoinOptions, get_option_and_weight, get_options_and_weights
from placenamegen.config import Config


def add_suffix(s: str, suffix: str) -> str:
    assert not suffix[0].isupper()
    assert not all(c.isspace() for c in s)
    assert not all(c.isspace() for c in suffix)
    # Remove consecutive same letters.
    if s[-1] == suffix[0]:
        suffix = suffix[1:]
        return add_suffix(s, suffix)
    if suffix in s:
        # Don't allow the same affix multiple times.
        return s
    return f'{s}{suffix}'


def random_selection(choices: Iterable[str], probability: float, random: Random, minimum: int = 0) -> list[str]:
    result: list[str] = []
    remaining_choices = list(choices)
    i = 0
    while remaining_choices and (random.random() < probability or len(result) < minimum):
        selection = random.choice(remaining_choices)
        result.append(selection)
        remaining_choices.remove(selection)
        probability *= exp(-(i + 1))
        i += 1
    return result


def select_affixes(affixes: JoinOptions, base_probability: float, random: Random, minimum: int = 0) -> list[str]:
    result: list[str] = []
    start_idx = random.randrange(len(affixes))

    probability = base_probability
    for i, level in enumerate(affixes[start_idx:]):
        raw_options, level_weight = get_option_and_weight(level)
        if random.random() < probability * level_weight or len(result) < minimum:
            options, weights = get_options_and_weights(raw_options)
            result.append(random.choices(options, weights)[0])
            probability *= exp(-(i + 1))
    return result


def generate_place_name(config: Config, random: Random = Random()) -> str:
    bases, base_weights = get_options_and_weights(config.bases)
    base = random.choices(bases, base_weights)[0]

    before_words = select_affixes(config.before_words, config.before_word_probability, random)

    if base.after.affix_allowed:
        after_affixes = select_affixes(
            config.after_affixes, config.after_affix_probability, random, int(base.after.affix_required(False)))
    else:
        after_affixes = []
    
    if base.after.word_allowed:
        required = base.after.word_required(bool(after_affixes))
        after_words = select_affixes(
            config.after_words, config.after_word_probability, random, int(required))
    else:
        after_words = []

    main_word = base.string
    for after_affix in after_affixes:
        main_word = add_suffix(main_word, after_affix)
    words = [main_word]
    for before_word in reversed(before_words):
        words.insert(0, before_word)
    for after_word in after_words:
        words.append(after_word)
    name = ' '.join(word.capitalize() for word in words)

    return name
