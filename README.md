# scholar

A collection of scripts to grab author data from scopus.com

## Usage

* `pip install elsapy` 
* In the same folder as `get_author_info.py`, create a `config.json` file and add your APIkey to it:
    ```json
    {
	    "apikey": "ENTER_APIKEY_HERE",
	    "insttoken": "ENTER_INSTTOKEN_HERE_IF_YOU_HAVE_ONE_ELSE_DELETE"
    }
    ```
    APIkey is obtained from [dev.elsevier.com](http://dev.elsevier.com). If you don't have a valid insttoken (which you would have received from Elsevier support staff), delete the placeholder text.

* Create a `authors.json` file containing a list of author names or author Scopus IDs to get metrics for. Use he following format:
    ```json
    {
        "ids": [
            "7006082359",
            "7407828513",
            "7101712642"
        ],
        "names": [
            ["Reg", "Bott"],
            ["James", "Clark"],
            ["Charles", "Cooney"]
        ]
    }
    ```
    If you wish to search by ID you can delete the "names" list or leave it empty.

* Run `python author_search.py` if you wish to search author by names or run `python get_author_by_id.py` if you wish to search by author Scopus ID.

* Follow the on screen instructions.

## Notes

#### On why author metric from author retrieval API differs from scopus.com:

The Author Profile page in the Scopus web interface calculates author metrics on-the-fly from a constantly updated database. Author metrics returned by the Author Retrieval API are fetched from a different database, which is updated every few weeks. 

Furthermore, this database only uses content published from 1996 onwards, which is why authors who have published prior to 1996 will show lower metrics through the API. All other data returned through the APIs is in sync with scopus.com. 

Ref: [Elsevier developer FAQ](https://dev.elsevier.com/tecdoc_developer_faq.html)
