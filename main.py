import math
import os
import sys
from datetime import datetime, date
from collections import namedtuple

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape, StrictUndefined
import requests
from requests.auth import HTTPBasicAuth
import click

"""We are interested only in invoices with this 'kod plneni' """
SUPPLY_CODE = 3

Period = namedtuple('Period', 'year month')
FakturoidAuth = namedtuple('FakturoidAuth', 'slug email apikey')


def get_all_invoices_for(period: Period, auth: FakturoidAuth):
    url = f'https://app.fakturoid.cz/api/v2/accounts/{auth.slug}/invoices.json'
    r = requests.get(url, auth=HTTPBasicAuth(auth.email, auth.apikey))
    invoices_all = r.json()

    def has_relevant_supply_code(invoice):
        return invoice['supply_code'] == str(SUPPLY_CODE)

    def is_issued_in_period(invoice):
        issued_on = datetime.strptime(invoice['issued_on'], '%Y-%m-%d')
        return issued_on.year == period.year and issued_on.month == period.month

    invoices = list(filter(lambda i: has_relevant_supply_code(i)
                                     and is_issued_in_period(i),
                           invoices_all))
    return invoices


def invoices_to_report_lines(invoices):
    clients_vat_no = set(map(lambda i: i['client_vat_no'], invoices))

    def extract_invoices_for(client_vat_no):
        return list(filter(lambda i: i['client_vat_no'] == client_vat_no, invoices))

    def extract_total_for(client_vat_no):
        # the report needs values in CZK
        sum_raw = sum(map(lambda i: float(i['native_total']), extract_invoices_for(client_vat_no)))
        return math.ceil(sum_raw)   # the form requires to round up

    lines = [{'vat_numeric_part': client_vat_no[2:],
              'vat_country_code': client_vat_no[0:2],
              'invoiced_total': extract_total_for(client_vat_no),
              'invoices_count': len(extract_invoices_for(client_vat_no)),
              'supply_code': SUPPLY_CODE,
              'line_no': index
              } for index, client_vat_no in enumerate(clients_vat_no, start=1)]
    return lines


def read_static_details(filepath):
    with open(filepath) as filepath:
        return yaml.load(filepath, Loader=yaml.FullLoader)


def generate_report(period: Period, report_lines, static_details):
    env = Environment(loader=FileSystemLoader('templates'),
                      autoescape=select_autoescape(['xml']),
                      undefined=StrictUndefined)    # raise error if var undefined

    template = env.get_template('souhrne_hlaseni.xml')
    signed_on = date.today().strftime("%d.%m.%Y")
    print(template.render(lines=report_lines,
                          period=period,
                          env=os.environ,
                          signed_on=signed_on,
                          static=static_details))


@click.command()
@click.option('--year', help='Year when invoices were issued', required=True, type=int)
@click.option('--month', help='Month when invoices were issued', required=True, type=int)
@click.option('--fakturoid-api-key', help='Your Fakturoid API key', required=True, type=str)
@click.option('--fakturoid-email', help='Your Fakturoid email', required=True, type=str)
@click.option('--fakturoid-slug', help='Your Fakturoid slug', required=True, type=str)
@click.option('--path-to-static-details', help='Path to an .ini file with your static details', required=True, type=click.Path(exists=True))
def main(year, month, fakturoid_api_key, fakturoid_email, fakturoid_slug, path_to_static_details):
    period = Period(year=year, month=month)
    auth = FakturoidAuth(
        slug=fakturoid_slug,
        email=fakturoid_email,
        apikey=fakturoid_api_key)
    invoices = get_all_invoices_for(period, auth)
    report_lines = invoices_to_report_lines(invoices)
    static_details = read_static_details(path_to_static_details)
    generate_report(period, report_lines, static_details)
    print('Now upload the report via https://adisspr.mfcr.cz/dpr/adis/idpr_epo/epo2/uvod/vstup_expert.faces', file=sys.stderr)


if __name__ == '__main__':
    main(auto_envvar_prefix='DPHSH')
