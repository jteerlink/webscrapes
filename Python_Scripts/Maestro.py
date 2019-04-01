
import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('/subscripts/Carrier_Scrape1.py', '/subscripts/Carrier_Scrape2.py','/subscripts/Carrier_Scrape3.py','/subscripts/Carrier_Scrape4.py'
'/subscripts/Carrier_Scrape5.py','/subscripts/Carrier_Scrape6.py','/subscripts/Carrier_Scrape7.py','/subscripts/Carrier_Scrape8.py')                                    

                                                  
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=8)                                                        
pool.map(run_process, processes) 