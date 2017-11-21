import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('NIFTY and NIFTY_Pharma.csv',index_col=0,parse_dates = True)
print data.head(5)

plt.figure(figsize=(10,9))
plt.subplot(211)
plt.plot(data['NIFTY'], lw=1, label ='NIFTY')
plt.grid(True)
plt.legend(loc=0)
plt.xticks(rotation=35)
plt.axis('tight')
plt.title('NIFTY Pharma Vs NIFTY')

plt.subplot(212)
plt.plot(data['NIFTY_Pharma'],lw=1, color='red', label ='NIFTY Pharma')

# 18th Oct
plt.annotate('US Pricing Pressure News',ha = 'center', va = 'bottom',xytext = ('10/21/2016', 11150),xy = ('10/18/2016', 11469.5),
arrowprops = { 'facecolor' : 'black', 'shrink' : 0.05 })

# 5th Nov
plt.annotate('US Probe Pressure News',ha = 'center', va = 'bottom',xytext = ('11/3/2016', 11000),xy = ('11/7/2016', 10818.8),
arrowprops = { 'facecolor' : 'black', 'shrink' : 0.05 })

# 10th Nov
plt.annotate('Trumps "Make in US" News Worries the Sector',ha = 'center', va = 'bottom',xytext = ('11/9/2016', 11325),xy = ('11/10/2016', 10990.6),
arrowprops = { 'facecolor' : 'black', 'shrink' : 0.05 })

# 16 nov
plt.annotate('Rising US Approvals News',ha = 'center', va = 'bottom',xytext = ('11/15/2016', 10950),xy = ('11/16/2016', 10559.3),
arrowprops = { 'facecolor' : 'black', 'shrink' : 0.05 })

plt.grid(True)
plt.legend(loc=0)
plt.xticks(rotation=35)
plt.axis('tight')





