from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor
import json
import csv


CONFIG_FILE_PATH = 'config.json'
BASE_AUTHOR_URI = 'https://api.elsevier.com/content/author/author_id/'


def authenticate():
    # Load configuration
    with open(CONFIG_FILE_PATH) as con_file:
        config = json.load(con_file)

    # Initialize client
    client = ElsClient(config['apikey'])
    client.inst_token = config['insttoken']

    return client


def get_author_by_id(client, author_id):
    author_data = dict()

    my_auth = ElsAuthor(uri=f"{BASE_AUTHOR_URI}{author_id}")

    if my_auth.read(client):
        my_auth.read_metrics(client)

        field_str = ''
        field_list = []
        for area in my_auth.data['subject-areas']['subject-area']:
            field_str += f"{area['$']} | "
            field_list.append(area['$'])

        author_data['name'] = my_auth.full_name
        author_data['url'] = my_auth.data['coredata']['link'][0]['@href']
        author_data['orcid'] = my_auth.data['coredata']['orcid']
        author_data['h-index'] = my_auth.data['h-index']
        author_data['docs'] = my_auth.data['coredata']['document-count']
        author_data['cit'] = my_auth.data['coredata']['citation-count']
        author_data['fields'] = field_list
        author_data['first-pub'] = my_auth.data['author-profile']['publication-range']['@start']
        author_data['pub-range'] = my_auth.data['author-profile']['publication-range']
        try:
            author_data['affiliation'] = {
                'name': my_auth.data['author-profile']['affiliation-current']['affiliation']['ip-doc']['preferred-name']['$'],
                'country': my_auth.data['author-profile']['affiliation-current']['affiliation']['ip-doc']['address']['country'],
                'url': my_auth.data['author-profile']['affiliation-current']['affiliation']['ip-doc']['org-URL']
            }
        except KeyError:
            author_data['affiliation'] = {
                'name': '',
                'country': '',
                'url': ''
            }

        # Print data
        print(f"Full name: {author_data['name']}")
        print(f"Link: {author_data['url']}")
        print(f"h-index: {author_data['h-index']}")
        print(f"Documents: {author_data['docs']}")
        print(f"Citations: {author_data['cit']}")
        print(f"First publication: {author_data['first-pub']}")
        print(f"Fields of study: {', '.join(author_data['fields'][:5])}")
        return author_data

    else:
        print("Read author failed.")
        return None


if __name__ == '__main__':
    cli = authenticate()

    get_author_by_id(cli, 54987869500)
