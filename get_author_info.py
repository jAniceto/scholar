"""
ON WHY AUTHOR METRIC FROM AUTHOR RETRIEVAL API DIFFER FROM SCOPUS.COM:

The Author Profile page in the Scopus web interface calculates author metrics on-the-fly from a constantly updated database. Author metrics returned by the Author Retrieval API are fetched from a different database, which is updated every few weeks. 

Furthermore, this database only uses content published from 1996 onwards, which is why authors who have published prior to 1996 will show lower metrics through the API. All other data returned through the APIs is in sync with www.scopus.com. 

Ref: https://dev.elsevier.com/tecdoc_developer_faq.html
"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor
from elsapy.elssearch import ElsSearch
import json
import csv


# AUTHOR_LIST = ['7005209482',
#                 '7102638942',
#                 '35502091400',
#                 '35413314000',
#                 '7203016479',
#                 '7102165550',
#                 '35109024200',
#                 '7201905260',
#                 '7201534122',
#                 '35598739000',
#                 '6602264945',
#                 '7005206227',
#                 '7103157456',
#                 '24492122900',
#                 '57200173922',
#                 '26643558900',
#                 '7102525310']

with open('authors.json', 'r') as fp:
    data = json.load(fp)
    AUTHOR_LIST = data['ids']


def get_author(client, author):  
    author_data = {}

    my_auth = ElsAuthor(uri=f"https://api.elsevier.com/content/author/author_id/{author}")
    
    if my_auth.read(client):
        my_auth.read_metrics(client)
        my_auth.read_docs(client)

        field_str = ""
        field_list = []
        for area in my_auth.data['subject-areas']['subject-area']:
            field_str += f"{area['$']} | "
            field_list.append(area['$'])
    
        author_data['name'] = my_auth.full_name
        author_data['url'] = my_auth.data['coredata']['link'][0]['@href']
        author_data['h-index'] = my_auth.data['h-index']
        author_data['docs'] = my_auth.data['coredata']['document-count']
        author_data['cit'] = my_auth.data['coredata']['citation-count']
        author_data['fields'] = field_list
        author_data['pub-range'] = my_auth.data['author-profile']['publication-range']
        try:
            author_data['affiliation'] = {'name': my_auth.data['author-profile']['affiliation-current']['affiliation']['ip-doc']['preferred-name']['$'],
                                          'country': my_auth.data['author-profile']['affiliation-current']['affiliation']['ip-doc']['address']['country'],
                                          'url': my_auth.data['author-profile']['affiliation-current']['affiliation']['ip-doc']['org-URL']}
        except KeyError:
            author_data['affiliation'] = {'name': '',
                                          'country': '',
                                          'url': ''}

        # print(author_data)
        
        return author_data
    
    else:
        print ("Read author failed.")


def cmd_print(data):
    # Print data
    print('')
    print(f"Full name: {data['name']}")
    print(f"Link: {data['url']}")
    print(f"h-index: {data['h-index']}")
    print(f"Documents: {data['docs']}")
    print(f"Citations: {data['cit']}")
    print(f"Fields of study: {data['fields'][:3]}")


def csv_save(data):
    # Save to csv
    with open('author-info.csv', 'w', encoding='UTF-8', newline='') as output_file:
        field_names = ['name', 'h-index', 'docs', 'cit', 'url', 'fields']  # fields to print to csv
        writer = csv.DictWriter(output_file, fieldnames=field_names)   

        writer.writeheader() 
        for row in data:
            row_to_print = {key: value for key, value in row.items() if key in field_names}
            writer.writerow(row_to_print)


def main():
    ## Load configuration
    with open("config.json") as con_file:
        config = json.load(con_file)

    ## Initialize client
    client = ElsClient(config['apikey'])
    client.inst_token = config['insttoken']

    print('Author count: {}'.format(len(AUTHOR_LIST)))

    all_data = []
    for author in AUTHOR_LIST:
        data = get_author(client, author)
        all_data.append(data)
        cmd_print(data)

    csv_save(all_data)

if __name__ == "__main__":
    main()
