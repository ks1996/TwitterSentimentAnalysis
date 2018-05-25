# Python code to take current BITCOIN prices 
import time, json, requests
import datetime
#import numpy as np
import matplotlib.pyplot as plt
now = datetime.datetime.now()
plt.ion()
count = 0

# Using Coinbase to take the btc prices 
def coinbase():
    coinBaseTick = requests.get('https://coinbase.com/api/v1/prices/buy') # live bitcoin prices in USD
    return coinBaseTick.json()['amount'] 

#Converting the unix timestamp to Time and saving it with the btcPrices
while True:
    coinbUSDLive = float(coinbase())
    print "Coinbase Price in USD =", coinbUSDLive
    posix_time = time.time()
    unix_timestamp  = int(posix_time)
    utc_time = time.gmtime(unix_timestamp)
    local_time = time.localtime(unix_timestamp) 
    fp = open('btcPrice3.txt','a')
    fpp = str(time.strftime("%H:%M:%S", local_time)+ '|'+ str(coinbUSDLive)).encode('utf-8')
    fp.write(fpp)
    fp.write('\n')
    fp.close()
    # After every 30 seconds
    time.sleep(30)
    
    
 
