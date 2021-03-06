factors = [
    {
        'name': 'province',
        'data': ['CABA', 'Buenos Aires', 'Catamarca', 'Cordoba', 'Corrientes', 'Chaco', 'Chubut',
                 'Entre Rios', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquen',
                 'Rio Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero',
                 'Tierra del Fuego', 'Tucuman', 'NA']
    }, {
        'name': 'company_size',
        'data': ['0-10', '11-50', '51-200', '201-1000', '1001+']
    }
]

quarters = ['Q1-04', 'Q2-04', 'Q3-04', 'Q4-04', '04', 'Q1-05', 'Q2-05', 'Q3-05', 'Q4-05', '05',
            'Q1-06', 'Q2-06', 'Q3-06', 'Q4-06', '06', 'Q1-07', 'Q2-07', 'Q3-07', 'Q4-07', '07', 'Q1-08',
            'Q2-08', 'Q3-08', 'Q4-08', '08', 'Q1-09', 'Q2-09', 'Q3-09', 'Q4-09', '09', 'Q1-10', 'Q2-10',
            'Q3-10', 'Q4-10', '10', 'Q1-11', 'Q2-11', 'Q3-11', 'Q4-11', '11', 'Q1-12', 'Q2-12', 'Q3-12',
            'Q4-12', '12', 'Q1-13', 'Q2-13', 'Q3-13', 'Q4-13', '13', 'Q1-14', 'Q2-14', 'Q3-14', 'Q4-14', '14',
            'Q1-15', 'Q2-15', 'Q3-15', 'Q4-15', '15', 'Q1-16', 'Q2-16']


def get_factor_by_name(name):
    return next(f for f in factors if f['name'] == factor)


def remove_thousands_separator(lines):
    """Remove thousands separator.
    e.g. 1,000,00 becomes 1000000
    """
    return map(lambda s: s.replace(',', '').rstrip(), lines)


def is_quarter(string):
    """Determine if measurement label is quarterly."""
    return string.startswith('Q')


def format_csv(factor_name, entry):
    """Format a data entry as a csv line."""
    return "%s, %s, %s" % (entry[factor_name], entry['quarter'], entry['count'])


def format_json(factor_name, entry):
    """Format a data entry as a json object."""
    return '{ "%s": "%s", "quarter": "%s", "count": "%s" }' % (
        factor_name, entry[factor_name], entry['quarter'], entry['count'])


def check_factor_size(factor, lines):
    """Fail if factor can't be applied to the given lines"""
    factor_l = len(factor['data'])
    lines_l = len(lines)
    if factor_l != lines_l:
        raise ValueError(
            'Chosen factor "%s" has %d items, and there are %d lines' %
            (factor['name'], factor_l, lines_l))


def create_data_structure(lines, factor_name):
    """Add chosen factor data to measurements."""
    data = []
    for i, line in enumerate(lines):
        factor_chosen = get_factor_by_name(factor_name)
        factor = factor_chosen['data'][i]

        # make sure factor chosen is adecuate for the input data
        check_factor_size(factor_chosen, lines)

        measures = line.split()
        for j, m in enumerate(measures):
            quarter = quarters[j]

            # avoid year means.
            if not is_quarter(quarter):
                continue
            data.append({factor_chosen['name']: factor, 'quarter': quarter, 'count': m})
    return data


import sys
from functools import partial

# check if we have standard input.
if sys.stdin.isatty():
    print "usage: cleanup_provinces.py < [input.txt]"
    exit(1)

lines = sys.stdin.readlines()
no_separator = remove_thousands_separator(lines)

factor = 'company_size'
data = create_data_structure(no_separator, factor)
fmt = partial(format_csv, factor)
csv = map(fmt, data)
for item in csv:
    print item
