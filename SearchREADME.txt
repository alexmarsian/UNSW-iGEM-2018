This is the documentation for the UNSW iGEM 2018 team's search tool, built to operate on the iGEM parts database.

The iGEM parts main page is available here: http://parts.igem.org/Main_Page 

This tool is not designed to replace the database, but rather be used in conjunction with the database, 
allowing users to apply multiple search filters to look for parts that meet specific search criteria.
Multi-parameter, and negative searches are possible using the tool.
From the parts returned by a search, users can look up the parts in the registry for more detail. 
Currently the tool only returns the name (BBa ID) of parts that meet the user-specified search criteria. 

Set Up:

Download the parts.xml file and place it in a folder.
Download the search.py file and place it in the same folder.
The tool runs using python 3, making use of the argparse and lxml modules. 
To install python 3, go here: https://www.python.org/downloads/
Other methods of installation are available: https://realpython.com/installing-python/ 
The recommended option is to install python via anaconda: https://conda.io/docs/user-guide/install/download.html 

Usage:
All commands here are executed following a call to the file. 
On my computer this looks like: ./search.py arguments values 
  For example: ./search.py -t RBS -r Issues F -m atgtaatgat
  
Type -h to see a list of possible commands the tool accepts.
To use the tool, enter an arugment, followed by it's value.
For example, to look for part's whose type is "RBS" (Ribosome Binding Site), type -t to denote part type followed by RBS:
  -t RBS
Currently, only one value is accepted for each argument. However negative searches can be conducted for any argument value.
To conduct a negative search, specify the argument, followed by the value, followed by F to denote 'False'.
For example, to look for part's whose results did NOT fail, type -r Fails F
  -r Fails F
Note that the argument values are case sensitive and must be exact, spelling errors are not tolerated.

There are some inconsistencies in the way information is stored in the parts database, with arbitrary argument values present in some parts.
For the author, and description arguments, again only a single argument value is accepted for now. Thus to look for all parts with author Alexander Pluto, one could enter either Alexander, or Pluto as the argument value - in most cases, using the author's surname will return a more accurate result. E.g. -a pluto
For a full list of possible argument values for each argument, see the values.txt file.
Each of the values present in the values.txt file is present at least once in the database, thus each should return at least 1 part.
This file was generated using the generate_values.py file, and contains every non-redundant instance of an argument value in the database. 

Special Notes: Negative searching of sequences and motifs
Searching for a sequence using the -s argument entails looking for exact sequence matches.
Thus searches of -s will return all of the twins for a particular part. 
In the 38,000 part database, a particular part may only have a handful of twins, thus negative searching on sequences is not reccommended. 
A negative sequence search (-s sequence F) will return every other part in the database that does not match the query sequence.
This will be many thousands of parts. If conducting a negative sequence search, it is reccommended to use other arguments alongside.
E.g. -s atgatgtcatcatcgatg F -r Works -t RBS etc. 
This will narrow the search space and prevent a very large number of parts being returned.
The same applies for motifs, if the query motif is very long and a negative search is conducted, many parts will be returned.
On the other hand, if a negative search is conducted with a very short query motif, almost no parts will be returned as 
the chance of any part containing a short motif such as atg is high. 

Any questions or suggestions can be sent to a%d%ma%rs.96@gma%il.com (Alex) - Remove the % chars! They simply prevent spam! :) 

The current list of accepted arguments (10/2018): 
-id [ [ ...]], --partID [ [ ...]]
                        BBa IDs for part (0 or more accepted)
  -t [ [ ...]], --partType [ [ ...]]
                        Part Category
  -r [ [ ...]], --partResults [ [ ...]]
                        One of "Works", "Issues", or "Fails"
  -rl [ [ ...]], --partRelease [ [ ...]]
                        The release status for a part
  -ss [ [ ...]], --partStatus [ [ ...]]
                        The sample status for a part
  -a [ [ ...]], --partAuthor [ [ ...]]
                        The author for a part
  -d [ [ ...]], --partDesc [ [ ...]]
                        Short description for the part
  -s [ [ ...]], --partSequence [ [ ...]]
                        Will only return exact matches
  -m [ [ ...]], --sequenceMotif [ [ ...]]
                        Short sequence motif


