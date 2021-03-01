import pandas as pd

data = {
    'name': ['yotta', 'zetta', 'exa', 'peta', 'tera', 'giga', 'mega', 'kilo', 'hecto', 'deka', 'base', 'deci', 'centi',
             'milli', 'micro', 'nano', 'pico', 'femto', 'atto', 'zepto', 'yocto'],
    'prefix': ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k', 'h', 'da', '-', 'd', 'c', 'm', 'u', 'n', 'p', 'f', 'a', 'z',
               'y'],
    'value': [10 ** 24, 10 ** 21, 10 ** 18, 10 ** 15, 10 ** 12, 10 ** 9, 10 ** 6, 10 ** 3, 10 ** 2, 10 ** 1, 10 ** 0,
              10 ** -1, 10 ** -2, 10 ** -3, 10 ** -6, 10 ** -9, 10 ** -12, 10 ** -15, 10 ** -18, 10 ** -21, 10 ** -24]}
metric_prefixes = pd.DataFrame(data=data).set_index('prefix')


def metric_convert(value: float, from_prefix: str, to_prefix: str) -> float:
    """ Converts the value to a different metric prefix.

    Metric prefixes to be chosen from:

    ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k', 'h', 'da', '-', 'd', 'c', 'm', 'u', 'n', 'p', 'f', 'a', 'z', 'y'].

    Where '-' is the base unit.

    :param value: The value to be converted.
    :param from_prefix: The metric prefix of the current value's unit.
    :param to_prefix: The metric prefix the value's unit should be in.
    :return: The converted value.
    """
    if not (from_prefix in metric_prefixes.index and to_prefix in metric_prefixes.index):
        raise ValueError('from_prefix and to_prefix should be valid metric prefixes')
    scale_factor = metric_prefixes.loc[from_prefix]['value'] / metric_prefixes.loc[to_prefix]['value']
    return value * scale_factor
