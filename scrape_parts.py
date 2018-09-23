#! /Users/Amarsing/anaconda3/bin/python

# Take xls file and create list of Part IDs that have been manually curated

# File Description
# This program takes a list of part IDs for the iGEM registry of parts
# and scrapes their xml format to build a singular xml file
# The task is run in batches
# The program requires a file in your directory containing part IDs
# The get_partids.py program retrieves IDs from an xml dump on the iGEM API
# Note the url is built based on the method described by the iGEM registry API
# The API is available here: http://parts.igem.org/Registry_API

import requests
import os.path


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

# Store the end line position as the start line position for the next batch
