#! /Users/Amarsing/anaconda3/bin/python

from lxml import etree

tree = etree.parse('parts.xml')

values = {'part_type': None, 'release_status': None, 'sample_status': None, 'part_results': None}

for key in values:
    values[key] = tree.xpath("//%s/text()" % key)
    values[key] = list(set(values[key]))

with open("values.txt", 'w') as f:
    f.write("This file contains all the values that may be entered for the listed arguments")
    for key in values:
        f.write("\n\nAll values for %s\n" % key)
        for item in values[key]:
            f.write(item + "\n")

