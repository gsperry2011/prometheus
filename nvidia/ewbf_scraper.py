#import the library used to query a website
import urllib2

#specify the url
url = "http://10.250.1.100:42000"

page = urllib2.urlopen(url)

from bs4 import BeautifulSoup

soup = BeautifulSoup(page, "lxml")

# The 'Statistcs of the GPUs' Table from webpage
statistics_table = soup.find('table', id='gpu_stat')


# Used to store our stats scraped from the table.
gpu_statistic_array = []

# Tracking current GPU ID
current_gpu = 0

for table_row in statistics_table:

    # what we will search the table_row for
    gpu_id = 'gpu' + str(current_gpu)

    # converting from bs4.tag to string to be checked for gpu_id
    current_row = str(table_row)

    # find rows containing GPUs
    if gpu_id in current_row:

#        print 'the table_row is:'
#        print table_row
        print '\n'

        # must target table_row and not current_row as find_all requires the bs4 object.
        gpu_stats = table_row.find_all('td')

        # setting variables for sanity. this removes the final <td> tag and contains the actual data only.
        gpu_name = gpu_stats[0].text
        gpu_temp = gpu_stats[1].text
        gpu_power = gpu_stats[2].text
        gpu_speed = gpu_stats[3].text
        gpu_efficiency = gpu_stats[4].text
        gpu_acceptedshares = gpu_stats[5].text
        gpu_rejectedshares = gpu_stats[6].text

        print gpu_name, gpu_temp, gpu_power, gpu_speed, gpu_efficiency, gpu_acceptedshares, gpu_rejectedshares
        
        # increment to go to next GPU
        current_gpu = current_gpu + 1
    

print gpu_statistic_array
