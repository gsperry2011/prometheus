#import the library used to query a website
import urllib2

#########################
#specify the url to scrap
url = "http://10.250.1.100:42000"

# file to write output for prometheus to read
outputfile = '~/testoutput.txt'



#########################

page = urllib2.urlopen(url)

from bs4 import BeautifulSoup

soup = BeautifulSoup(page, "lxml")

# The 'Statistcs of the GPUs' Table from webpage
statistics_table = soup.find('table', id='gpu_stat')


# Used to store our stats scraped from the table.
gpu_statistic_array = []

# Tracking current GPU ID
current_gpu = 0

# open our file for writing. It will overwrite the next time we open it.
with open('%outputfile', 'w') as output:

    for table_row in statistics_table:

        # what we will search the table_row for
        gpu_id = 'gpu' + str(current_gpu)

        # converting from bs4.tag to string to be checked for gpu_id
        current_row = str(table_row)
        
        # find rows containing GPUs
        if gpu_id in current_row:

        
            # must target table_row and not current_row as find_all requires the bs4 object.
            gpu_stats = table_row.find_all('td')
            
            # writing output to file. lines will not be trampled as we keep the file open for the duration of the script run.
            output.write( "gpu_name: %s, gpu_temp: %s, gpu_power: %s, gpu_speed: %s, gpu_efficiency: %s, gpu_acceptedshares: %s, gpu_rejectedshares: %s\n" % \
                       (gpu_stats[0].text,
                        gpu_stats[1].text,
                        gpu_stats[2].text,
                        gpu_stats[3].text,
                        gpu_stats[4].text,
                        gpu_stats[5].text,
                        gpu_stats[6].text))

        
            # increment to go to next GPU
            current_gpu = current_gpu + 1
        
