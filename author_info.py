"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor
from elsapy.elssearch import ElsSearch
import json
import csv


def save_info(myData):
    with open('author-info.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(myData)

    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']

# author_list = ['7006352812']

author_list = ['7005209482',
               '7102638942',
               '35502091400',
               '35413314000',
               '7203016479',
               '7102165550',
               '35109024200',
               '7201905260',
               '7201534122',
               '35598739000',
               '6602264945',
               '7005206227',
               '7103157456',
               '24492122900',
               '57200173922',
               '26643558900',
               '7102525310']

print('Author count: {}'.format(len(author_list)))


data = []

## Author example
# Initialize author with uri
for author in author_list:

    my_auth = ElsAuthor(
            uri = 'https://api.elsevier.com/content/author/author_id/{}'.format(author))
    
    if my_auth.read(client):
        my_auth.read_metrics(client)

        # print(my_auth.data)

        area_str = ''
        for area in my_auth.data['subject-areas']['subject-area'][:10]:
            area_str += '{} | '.format(area['$']) 
        
        
        # Print data
        print('')
        print("Full name: {}".format(my_auth.full_name))
        print("Link: {}".format(my_auth.data['coredata']['link'][0]['@href']))
        print("h-index: {}".format(my_auth.data['h-index']))
        print("Documents: {}".format(my_auth.data['coredata']['document-count']))
        print("Citations: {}".format(my_auth.data['coredata']['citation-count']))
        print("Fields of study: {}".format(area_str))
        
        # Save list to use in csv
        data.append([my_auth.full_name,
                     my_auth.data['h-index'],
                     my_auth.data['coredata']['document-count'],
                     my_auth.data['coredata']['citation-count'],
                     area_str,
                     my_auth.data['coredata']['link'][0]['@href']])
        
    else:
        print ("Read author failed.")

# Save to csv
save_info(data)
