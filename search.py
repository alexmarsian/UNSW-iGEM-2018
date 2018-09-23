#! /Users/Amarsing/anaconda3/bin/python

# CREATED FOR THE 2018 iGEM COMPETITION BY THE UNSW TEAM.
# Questions and suggestions can be submitted to ad%ma%rs.96%@g%mail.com
# Remove the % from the email!

# IMPORTANT: READ THE SearchREADME.TXT BEFORE USE PLEASE
# ENSURE THAT THE 'parts.xml' FILE IS IN THE SAME DIRECTORY AS THIS FILE


from lxml import etree
import argparse


# Define Arguments to be taken in at commandline
# Note that the destination names of the arguments are important for the speed of the search tool
parser = argparse.ArgumentParser(description='UNSW 2018 iGEM Database Search Tool', add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='To conduct a negative search on any '
                         'argument value FOLLOW the value with F or f E.g. -t RBS F will find all parts that are NOT '
                         'categorised as ribosome binding sites. The sequence -s, and motif -m arguments only '
                         'accept a single value, all other arguments accept multiple values. Note that the values for '
                         'the type argument are the most variable as the categories defined by iGEM in the database'
                         'are somewhat arbitrary')
parser.add_argument('-id', '--partID', type=str, nargs='*', dest="part_name", metavar='',
                    help='BBa IDs for part (0 or more accepted)')
parser.add_argument('-t', '--partType', type=str, nargs='*', dest='part_type', metavar='',
                    help='Part Category')
parser.add_argument('-r', '--partResults', nargs='*', type=str, dest='part_results', metavar='',
                    help='One of "Works", "Issues", or "Fails"')
parser.add_argument('-rl', '--partRelease', nargs='*', type=str, dest='release_status', metavar='',
                    help='The release status for a part')
parser.add_argument('-ss', '--partStatus', nargs='*', type=str, dest='sample_status', metavar='',
                    help='The sample status for a part')
parser.add_argument('-a', '--partAuthor', nargs='*', type=str, dest='part_author', metavar='',
                    help='The author for a part')
parser.add_argument('-d', '--partDesc', nargs='*', type=str, dest='part_short_desc', metavar='',
                    help='Short description for the part')
parser.add_argument('-s', '--partSequence', nargs='*', type=str, dest='seq', metavar='',
                    help='Will only return exact matches')
parser.add_argument('-m', '--sequenceMotif', nargs='*', type=str, dest='seq_data', metavar='',
                    help='Short sequence motif')


# Parse the Arguments into variables
args = vars(parser.parse_args())
if not any(args.values()):
    parser.error('No arguments provided. Run with -h for usage')

# Build the Tree to be searched with argument values
# If you name the parts.xml file provided on github something else, change the name below to correspond
tree = etree.parse('cleaned_file.xml')
root = tree.getroot()

crap = tree.xpath("//part/sample_status/text()[normalize-space(.)='Discontinued']/../..")

# Define the Fetch Function
# List of Strings, String, List of Element Objects, String -> List of Element Objects
# Refines the list of elements to be returned based on arguments handed to it
# Deals with sequence arguments separately
# If the search returns a long list of arguments, the result will be written to a file
# Otherwise the result is printed to the commandline (part_names only)


def fetch(arg_values, arg_key, current_tree):

    # Searching for parts that CONTAIN sequence motifs
    if arg_key in ("seq_data", "part_author", "part_short_desc"):
        if arg_values[-1] == 'F':
            fetched_parts = current_tree.xpath("//%s/text()[not(contains(normalize-space(.),'%s'))]"
                                               "/ancestor::part" % (arg_key, arg_values[0]))
        else:
            print(arg_values[0])
            fetched_parts = current_tree.xpath("//%s/text()[contains(normalize-space(.),'%s')]"
                                               "/ancestor::part" % (arg_key, arg_values[0]))
    # Search for parts whose sequence is an exact match to the query sequence
    elif arg_key == "seq":
        if arg_values[-1] == 'F':
            print("Finding non-matching sequences: This may take a while...")
            fetched_parts = current_tree.xpath("//part/sequences/seq_data/text()[not(normalize-space(.)='%s')]"
                                               "/ancestor::part" % (arg_values[0]))
        else:
            fetched_parts = current_tree.xpath("//part/sequences/seq_data/text()[normalize-space(.)='%s']"
                                               "/ancestor::part" % (arg_values[0]))
    # Search for all other parts that MATCH specified arguments
    else:
        if arg_values[-1] == 'F':
            fetched_parts = current_tree.xpath("//part/%s/text()[not(normalize-space(.)='%s')]/../.."
                                               "" % (arg_key, arg_values[0]))
        else:
            fetched_parts = current_tree.xpath("//part/%s/text()[normalize-space(.)='%s']/../.."
                                               "" % (arg_key, arg_values[0]))

    return fetched_parts


# For each argument parsed, create a list of all parts that match
# Compare the lists after all searches have been conducted for every argument
# Keep the common items between lists
# i.e. Keep parts that met all search criteria

results = {}

for key in args:
    if args[key] is not None:
        # Returns a list of element tree part objects
        parts = fetch(args[key], key, tree)  # At this stage the function works
        # Convert element tree objects to part names
        for i in range(0, len(parts)):
            parts[i] = parts[i].find("part_name").text
        results[key] = set(parts)


final = set.intersection(*results.values())
if len(final) > 50:
    print("%d parts met your search criteria. Find them in Results.txt" % len(final))
    with open("results.txt", 'w') as f:
        f.write("%d parts met your search criteria: %s\n" % (len(final), args))
        for part in final:
            f.write(part+"\n")
else:
    print(final)
    print("%d parts met your search criteria" % len(final))
