#! /Users/Amarsing/anaconda3/bin/python

import os

xmlfile = open('xml_parts.txt', 'rb')
newfile = open('igem_part_IDs2.txt', 'wb')

# From the XML dump at http://parts.igem.org/Registry_API
# Gather part IDs for use in web scraping
# Count the number of parts added
i = 0
for line in xmlfile:
    if line.lstrip().startswith(b'<field name="part_name"'):
        line = line.split(b'>', 1)[-1]
        line = line.split(b'<')[0]
        line = line + b'\n'
        newfile.write(line)
        i += 1
newfile.close()

# Remove replicate part IDs
# Delete the old file
lines_seen = set()  # holds lines already seen
outfile = open("part_ids.txt", "w")
count = 0
for line in open("igem_part_IDs2.txt", "r"):
    if line not in lines_seen:  # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
        count += 1
print("%d Non Redundant Part IDs generated: Find them in part_ids.txt" % count)
outfile.close()

os.remove("igem_part_IDs2.txt")
