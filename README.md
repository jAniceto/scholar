# scholar

A collection of scripts to grab author data from scopus.com

## Usage

* `pip install elsapy` 
* In your same folder as `get_author_info.py`, create a `config.json` file and add your APIkey to it:
    ```json
    {
	    "apikey": "ENTER_APIKEY_HERE",
	    "insttoken": "ENTER_INSTTOKEN_HERE_IF_YOU_HAVE_ONE_ELSE_DELETE"
    }
    ```
    APIkey is obtained from [dev.elsevier.com](http://dev.elsevier.com). If you don't have a valid insttoken (which you would have received from Elsevier support staff), delete the placeholder text.

* Insert the desired authors IDs in the `AUTHOR_LIST` varialble in the `get_author_info.py` file.

* Run `python get_author_info.py`.

