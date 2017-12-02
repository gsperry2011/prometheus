import os
import sys
import time
import prometheus_client
from prometheus_client import start_http_server, Metric, REGISTRY

# scrapes ewbf webpage and sanatizes data for consumption by prometheus.
# call this function with the GPU number you wish to return data for. Starting at 0.
def scrape_ewbf(current_gpu):

    import urllib2
    from bs4 import BeautifulSoup

    #specify the url to scrap
    url = "http://10.250.1.100:42000"
    
    page = urllib2.urlopen(url)
    
    soup = BeautifulSoup(page, "lxml")
    
    # The 'Statistcs of the GPUs' Table from webpage
    statistics_table = soup.find('table', id='gpu_stat')
    
    
    # Used to store our stats scraped from the table.
    gpu_statistic_array = []
    
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
        
            gpu_name = gpu_stats[0].text
        
            gpu_temp = gpu_stats[1].text
            gpu_temp = gpu_temp.split('C')
            gpu_temp = gpu_temp[0]

            gpu_power = gpu_stats[2].text
            gpu_power = gpu_power.split('W')
            gpu_power = gpu_power[0]
            
            gpu_speed = gpu_stats[3].text
            gpu_speed = gpu_speed.split('Sol/s')
            gpu_speed = gpu_speed[0]
            
            gpu_efficiency = gpu_stats[4].text
            gpu_efficiency = gpu_efficiency.split('Sol/W')
            gpu_efficiency = gpu_efficiency[0]
            
            gpu_acceptedshares = gpu_stats[5].text
            gpu_rejectedshares = gpu_stats[6].text

            return [gpu_name, gpu_temp, gpu_power, gpu_speed, gpu_efficiency, gpu_acceptedshares, gpu_rejectedshares]
        
            # increment to go to next GPU
            current_gpu = current_gpu + 1
            
        
# posting data to local http for prometheus to scrape
class ewbfcollector(object):

    def ___init___(self):
        pass

    def collect(self):

        count = 0

        while count < 3:
            payload = scrape_ewbf(count)
            gpu_name = payload[0]
            gpu_temp = payload[1]
            gpu_power = payload[2]
            gpu_speed = payload[3]
            gpu_efficiency = payload[4]
            gpu_acceptedshares = payload[5]
            gpu_rejectedshares = payload[6]
            
            metric = Metric(gpu_name, 'GPU temp', 'gauge')
            metric.add_sample('gpu_temp_celcius', value=float(gpu_temp), labels={})
            yield metric
            
            metric = Metric(gpu_name, 'GPU power', 'gauge')
            metric.add_sample('gpu_power_watts', value=float(gpu_power), labels={})
            yield metric
            
            metric = Metric(gpu_name, 'GPU hashrate Sol/s', 'gauge')
            metric.add_sample('gpu_hashrate', value=float(gpu_speed), labels={})
            yield metric
            
            metric = Metric(gpu_name, 'GPU efficiency Sol/W', 'gauge')
            metric.add_sample('gpu_efficiency', value=float(gpu_efficiency), labels={})
            yield metric
            
            metric = Metric(gpu_name, 'GPU accepted shares', 'gauge')
            metric.add_sample('gpu_acceptedshares', value=float(gpu_acceptedshares), labels={})
            yield metric
            
            metric = Metric(gpu_name, 'GPU rejected shares', 'gauge')
            metric.add_sample('gpu_rejectedshares', value=float(gpu_rejectedshares), labels={})
            yield metric

            count = count + 1


# start web server and post ewbf data        
if __name__ == "__main__":
    
    print 'starting web server...'
    start_http_server(8000)
    REGISTRY.register(ewbfcollector())
    while True: time.sleep(1)
