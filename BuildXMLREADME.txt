This file contains instructions for how to build the new xml file. 
This process has been automated by simply calling each of the scripts in a single file, 
all that needs to be done is to run the build.py file. 

Detailed information on how the file was built is presented below. 

1. Download the iGEM parts xml dump from here: http://parts.igem.org/Registry_API (Under xml point in time database dump)
2. Using a text editor (such as sublime text or textwrangler), open the xml file and resave it as a .txt file

Why is this necessary? 
The xml file available on the registry contains encoding issues and structural errors, 
for example, all of the nodes for sha1-restriction in each part are corrupted. 
Thus parsing the xml file using a pre-existing module is not possible. 
We are going to build a new xml file from scratch, but to do that we at least need the part IDs from the database.

3. Run the get_partids.py file
Note that the name of the .txt file must match the name of the input file found on line 5 in get_partids.py
For convenience, name the .txt file xml_parts.txt, then you won't need to change anything in the get_partids.py file!
This file will generate another file in the same directory - part_ids.txt

4. Run the scrape_parts.py file
This file will utilise the part_ids.txt file to fetch the xml for parts in the database from the relevant part URL.
E.g. the xml for part BBa_B004 is found here: http://parts.igem.org/cgi/xml/part.cgi?part=BBa_B0034
The scrape_parts.py file will build the new, clean xml by fetching the xml for 500 parts at a time.
These are batches of parts. The number of batches, and the size of each batch can be altered at the bottom of the scrape_parts.py file
The default is set to 80 batches of 500 parts (40,000 total), which covers the 38,000 part database. 
Note the file will remember what part was previously fetched, so if you only have time to fetch 5 batches at once, 
then the next time scrape_parts.py is run it will start from the last place. 
This is possible through the last_line_no.txt file - don't delete it unless you would like to scrape the parts from the beginning again.

scrape_parts.py will create a new file called parts.xml

5. Run the clean_tree.py file to remove errors that occur when building the file

You should now have a file called cleaned_file.xml which contains an up to date version of the iGEM parts database! 

