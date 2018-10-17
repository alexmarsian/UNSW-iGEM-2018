#! /Users/Amarsing/anaconda3/bin/python

import os
import requests

#### Getting a list of part IDs from the xml_parts.txt file ####

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


#### Scraping the Parts from the website using the Part IDs just created ####

print("Fetching the parts from the internet!")

# Take xls file and create list of Part IDs that have been manually curated

# File Description
# This program takes a list of part IDs for the iGEM registry of parts
# and scrapes their xml format to build a singular xml file
# The task is run in batches
# The program requires a file in your directory containing part IDs
# The get_partids.py program retrieves IDs from an xml dump on the iGEM API
# Note the url is built based on the method described by the iGEM registry API
# The API is available here: http://parts.igem.org/Registry_API


# def scraper
# File Int Boolean --> File
# Open a file of URL IDs, search the URLs
# Append the text at each URL into a file
# Remove unwanted chars that come with multiple URL requests

def scraper(file, batches: int, first_batch):

    newfile = open(name, 'a')

    for i in range(0, batches):

        if os.path.exists('last_line_no.txt'):
            with open('last_line_no.txt') as f:
                line_start = int(f.readline()) + 1
                first_batch = False
        else:
            line_start = 0
        print("%d Parts Collected" % line_start)

        # Open the file containing part ids
        with open(file, 'r') as f:

            # Create a url
            url = get_batch(f, batch_size, line_start)
            if url[1]:
                content = requests.get(url[0].strip())
                newfile.write(content.text)
                batches = 0
                break
            content = requests.get(url[0].strip())
            content = content.text
            if first_batch:
                # Add the content at the url to a newfile
                newfile.write(content[:-21])
                first_batch = False
            else:
                # Strip the xml encoding line, and root tags
                # These are pulled by requests in each batch
                # But should only be present at the very start and end
                # Of the xml fle
                content = content[144:-21]
                newfile.write('\n' + content)


# def get_batch
# File --> String
# Open a file containing IDs (1 per line)
# Create a batch of IDs to be searched

def get_batch(openfile, batch_size: int, line_start):

    # Find the correct starting line
    lines = openfile.read().split('\n')
    # Create the base URL
    url = base_url.strip() + lines[line_start].strip()
    # Add additional IDs for the desired batch size
    if batch_size > 1:
        if batch_size > (len(lines)-line_start):
            for line in lines[line_start+1:len(lines)]:
                url = url + '.' + line.strip()
            print('DONE!')
            return [url, True]
        else:
            for line in lines[line_start+1:(line_start+batch_size)]:
                url = url + '.' + line.strip()
    with open('last_line_no.txt', 'w') as last_line:
        last_line.write(str((batch_size + line_start)-1))
    return [url, False]


# Input required for functions (could make user input)
batch_size = 500
batches = 80
base_url = 'http://parts.igem.org/cgi/xml/part.cgi?part='
name = 'parts.xml'  # Name of the outfile

# Run one batch
scraper('part_ids.txt', batches, True)

print("Done fetching parts.")



#### Clean up the created XML ####

print("Cleaning Up the XML Tree")

infile = "parts.xml"
outfile = "cleaned_file.xml"

delete_list = ['<?xml version="1.0" encoding="utf-8" standalone="yes" ?>',
               "<rsbpml>", "<part_list>", "</h1>", "<p>The server encountered an internal error or",
                                          "misconfiguration and was unable to complete", "your request.</p>",
                                          "<p>Please contact the server administrator at",
                                          "root@localhost to inform them of the time this error occurred,",
                                          "and the actions you performed just before this error.</p>",
                                          "<p>More information about this error may be available",
                                          "in the server error log]"]
fin = open(infile)
fout = open(outfile, "w+")

for i, line in enumerate(fin):
    for word in delete_list:
        if i > 5:
            line = line.replace(word, "")
    fout.write(line)
fin.close()
fout.close()

print("Done. Cleaned XML file is now available in %s" % outfile)
