# Souhrnné hlášení VIES z Fakturoid 

Generate XML with "souhrne hlaseni" for a given month 
based on invoices from [Fakturoid](https://www.fakturoid.cz/).

The Python script fetches invoices with [Fakturoid v2 API](https://fakturoid.docs.apiary.io) 
and generates an XML report which can be [uploaded to 
Ministry of Finance]( https://adisspr.mfcr.cz/dpr/adis/idpr_epo/epo2/uvod/vstup_expert.faces)  

# Supported use cases
- summing up 2+ invoices for the same client
- generating lines for multiple clients
- proper numerical rounding of the line total 

# Unsupported use cases
- using supply code ("kod plneni") other than 3
- having tens of clients, leading to multipage report
- credit nootes 

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

# Example output

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Pisemnost nazevSW="EPO MF ČR" verzeSW="41.24.2">
    <DPHSHV verzePis="02.01">
        <VetaD
                k_uladis="DPH"
                dokument="SHV"
                rok="2020"
                mesic="5"
                shvies_forma="R"
                d_poddp="02.03.2021"
                />
        <VetaP
                c_ufo="450"
                c_pracufo="2000"
                dic="801010000"
                typ_ds="F"
                prijmeni="Doe"
                jmeno="John"
                titul="Bc."
                naz_obce="Praha"
                ulice="Vaclávské námestí"
                c_pop="1"
                c_orient="2"
                psc="10000"
                sest_prijmeni="Doe"
                sest_jmeno="John"
                sest_telef="725000111"
                stat="ČESKÁ REPUBLIKA"/>
        
            <VetaR
                por_c_stran="1"
                c_rad="1"
                k_stat="NL"
                c_vat="123456789012"
                k_pln_eu="3"
                pln_pocet="2"
                pln_hodnota="1000.0"/>
            </DPHSHV>
</Pisemnost>

```
# Using with fzf

You can also run the script wrapped with [fzf](https://github.com/junegunn/fzf) to select the month:

```shell
$ ./run-with-fzf.sh
```
