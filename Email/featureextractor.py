
################  Python 3.4  ####################
import json, csv
from pprint import pprint

heads = ['Delivered-To', 'From', 'Recieved', 'To', 'Message-ID', 'name', 'email', 'developer', 'Mailing-List', 'Body', 'X-Smam_Rating', 'List-Help', 'List-Unsubscribe','Subject']

with open('lucene-threads_sample.json',encoding='utf-8') as data_file:    
    data = json.load(data_file)

    ofile = open('EmployData.csv', "w")
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(heads)

    for d in data:
        emails = d['emails']
        for email in emails:
            try:
                delivered_to = email['Delivered-To']
            except:
                delivered_to = None
            try:		
                frm = email['From']
            except:
                frm = None
            try:	
                recieved = email['Recieved']
            except:
                recieved = None
            try:	
                to = email['To']
            except:
                to = None
            try:		
                message_id = email['Message-ID']
            except:
                message_id = None
            try:		
                name = email['author']['name']
            except:
                name = None
            try:	
                em = email['author']['email'][0]
            except:
                em = None
            try:		
                developer = email['author']['developer']
            except:
                developer = None
            try:	
                mailing_list = email['Mailing-List']
            except:
                mailing_list = None
            try:	
                body = email['Body']
            except:
                body = None
            try:		
                x_smam_rating = email['X-Spam-Rating']
            except:
                x_smam_rating = None	
            try:	
                list_help = email['List-Help']
            except:
                list_help =None
            try:		
                list_unsubscribe = email['List-Unsubscribe']
            except:
                list_unsubscribe = None
            try:	
                subject = email['Subject']
            except:
                subject = None

            r = (delivered_to,frm,recieved,to,message_id,name,em,developer,mailing_list,body,x_smam_rating,list_help,list_unsubscribe,subject)
            writer.writerow(r)		
