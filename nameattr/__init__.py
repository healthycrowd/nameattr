import importlib
import nltk


__version__ = "1.0.0"


_FIND_TYPES = ("text",)
_type_funcs = []


for find_type in _FIND_TYPES:

    def generate_func():
        module = importlib.import_module(f"._{find_type}", package=__name__)
        matches_func_name = f"matches_from_{find_type}"
        matches_func = getattr(module, matches_func_name)

        def func(*args, **kwargs):
            try:
                threshold = kwargs.pop("threshold")
            except KeyError:
                threshold = None
            return matches_func(*args, **kwargs).best_match(threshold)

        func_name = f"from_{find_type}"
        func.__name__ = func_name
        _type_funcs.append(func_name)

        return {
            matches_func_name: matches_func,
            func_name: func,
        }

    locals().update(generate_func())


__all__ = tuple(_type_funcs)


# This isn't great but needed until there's a better way to do this or nltk is replaced
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
