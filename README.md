# Electricity_measure
A script that will fetch the electricity usage data from a website and plot the last week's usage. The job.sh script contains the python script, but is also headed by the commands to run the script from the unix command line. This is so the script can be run automatically each day at a specified time, with crontab. For example, to run job.sh at 8am each day:

# First make the bash script executable
chmod u+x /path/to/job.sh

# Now open a crontab file on your user account and edit it with a text editor
crontab -e

# Specify the required variables in this file(time, user and path to executable script)

0 8 * * * felix /path/to/job.sh




# The electricity measurer can be used to scrape and then graph data from other URLs by making the following changes to the script:

myURL = 'Any URL'
specific_file = 'Any unique string identifier of a desired file contained on the URL'

The script filters out all 'invisible' HTML text from the website, and makes a list of files that are accessible for download in all_files. I've chosen to select a subset of these files based on date, but this filter can be changed by altering the selector_strings.
