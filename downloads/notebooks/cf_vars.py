# -*- coding: utf-8 -*-
#
# cf_vars.py
#
# purpose:
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/
# created:  29-Sep-2014
# modified: Mon 29 Sep 2014 06:44:55 PM BRT
#
# obs:
#


from xml.etree import ElementTree


def get_standard_names(hints, units, cf_table='cf-standard-name-table.xml'):
    """If `hints` and `units` are True return `standard_name` in the list.
    Searches for `hints` in the description+standard_name, searches and units
    in the canonical_units field."""

    standard_names = []
    tree = ElementTree.parse('cf-standard-name-table.xml')
    root = tree.getroot()
    entries = root.findall('entry')
    for entry in entries:
        standard_name = entry.get('id')
        canonical_units = entry.find('canonical_units').text
        description = entry.find('description').text
        if description:
            description = '{} {}'.format(description.lower(), standard_name)
        else:
            description = '{}'.format(standard_name)
        description = set(description.lower().strip().split())
        if (set(hints) < description and units == canonical_units):
            standard_names.append(standard_name)
    return standard_names

hints = ['temperature', 'sea']
units = 'K'
CF_names = get_standard_names(hints=hints, units=units)

print('\n'.join(CF_names))
