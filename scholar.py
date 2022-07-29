import json
import csv
import typer
from scopus import authenticate, get_author_by_id

app = typer.Typer()


@app.command()
def author_metrics(author: str = typer.Argument(None), file: bool = False):
    # Authenticate with Scopus
    client = authenticate()

    if author:
        try:
            # Author as Scopus ID
            scopusid = int(author)

        except ValueError as e:
            print('Provide author Scopus ID.')

        get_author_by_id(client, scopusid)

    elif file:
        # Load author ID list
        with open('authors.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            author_list = data['ids']

        # Get metrics
        data = []
        for scopusid in author_list:
            data.append(get_author_by_id(client, scopusid))
            print('')

        # Save CSV
        with open('author-info.csv', 'w', encoding='UTF-8', newline='') as output_file:
            field_names = ['name', 'orcid', 'h-index', 'docs', 'cit', 'first-pub', 'url', 'fields']  # fields to print to csv
            writer = csv.DictWriter(output_file, fieldnames=field_names)

            writer.writeheader()
            for row in data:
                row_to_print = {key: value for key, value in row.items() if key in field_names}
                writer.writerow(row_to_print)


@app.command()
def test():
    print('Teste')


if __name__ == "__main__":
    app()
