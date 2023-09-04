from rest_framework.routers import SimpleRouter
from spellchecker import SpellChecker


def get_router(name: str, view) -> list:
    r = SimpleRouter()
    r.register(name, view)
    return r.urls


def check_spell(words: str) -> str:
    spell = SpellChecker(language=['ru', 'en'], distance=1)

    words = remove_spaces(words)
    misspelled = spell.unknown(words.split(' ')).union(set([w.lower() for w in words.split(' ')]))

    result = []
    for word in misspelled:
        correction = spell.correction(word)
        result.append(correction if correction else word)

    return ' '.join(result)


def remove_spaces(value: str) -> str:
    value = str(value)
    splitted_value = list(value)

    pass_begin = False
    pass_end = False

    for _ in splitted_value:
        if not pass_begin:
            if splitted_value[0] == " ":
                del splitted_value[0]
            else:
                pass_begin = True

        if not pass_end:
            if splitted_value[-1] == " ":
                del splitted_value[-1]
            else:
                pass_end = True

        if pass_end and pass_begin:
            break

    return ''.join(splitted_value)