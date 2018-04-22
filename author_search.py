from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json

SEARCH_LIST = [['', 'Cardoso'],
               ['Marcelo', ''],
               ['', 'Aniceto']]

# Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

# Initialize client
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']

auth_id_list = []

for author in SEARCH_LIST:
    search_query = ""
    if len(author[0]) > 0:
        search_query += f"authfirst({author[0]}) "
    if len(author[1]) > 0:
        search_query += f"authlast({author[1]})"

    auth_srch = ElsSearch(search_query, 'author')
    auth_srch.execute(client)
    print(f'{author[0]} {author[1]}: {len(auth_srch.results)} results found!\n')

    # Display search results
    for i, search_result in enumerate(auth_srch.results):
        first_name = search_result['preferred-name']['given-name']
        surname = search_result['preferred-name']['surname']
        affiliation = search_result['affiliation-current']['affiliation-name']
        affiliation_country = search_result['affiliation-current']['affiliation-country']
        print(f"[{i+1}] {first_name} {surname}, {affiliation} ({affiliation_country})")

    # Choose desired author
    desired_author_index = int(input('\nChoose correct author: ')) - 1
    desired_author = auth_srch.results[desired_author_index]
    link = desired_author['link'][0]['@href']
    auth_id = desired_author['dc:identifier'].split(':')[1]

    auth_id_list.append(auth_id)

    print(link)
    print(auth_id)
