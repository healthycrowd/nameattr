import names
import random


random.seed(2)
MONONYM = names.get_first_name()
FULLNAME = names.get_full_name()
FULLNAME_MIDDLE = " ".join(
    [names.get_first_name(), names.get_first_name(), names.get_last_name()]
)
FULL_DOUBLE_PREFIXED_SURNAME = " ".join(
    [names.get_first_name(), "van", "der", names.get_last_name()]
)
FULL_SINGLE_PREFIXED_SURNAME = " ".join(
    [names.get_first_name(), "da", names.get_last_name()]
)
