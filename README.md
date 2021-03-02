# Souhrnné hlášení VIES z Fakturoid 

Generate XML with "souhrne hlaseni" for a given month 
based on invoices from [Fakturoid](https://www.fakturoid.cz/).

The Python script fetches invoices with [Fakturoid v2 API](https://fakturoid.docs.apiary.io) 
and generates an XML report which can be [uploaded to 
Ministry of Finance]( https://adisspr.mfcr.cz/dpr/adis/idpr_epo/epo2/uvod/vstup_expert.faces)  

### How to run

1. Clone the repo
2. Copy the YAML file and fill it with your details
3. Install & run the tool with:
   
    ```shell
    $ pip3 install -r requirements.txt
    $ export DPHSH_FAKTUROID_EMAIL='<your-email>'
    $ export DPHSH_FAKTUROID_SLUG='<your-api-slug>'
    $ export DPHSH_FAKTUROID_API_KEY='<your-api-key>'
    $ python3 main.py --help
    $ python3 main.py --year 2021 --month 3 --path-to-static-details=./my-static-data.yml > dphsh-2021-03.xml
    ```

# Using with fzf

You can also run the script wrapped with [fzf](https://github.com/junegunn/fzf) to select the month:

```shell
$ ./run-with-fzf.sh
```
