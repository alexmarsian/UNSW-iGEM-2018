#! /Users/Amarsing/anaconda3/bin/python


# Build the Tree to be searched with argument values
# If you name the parts.xml file provided on github something else, change the name below to correspond

infile = "parts2.xml"
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
