import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from bs4 import BeautifulSoup, SoupStrainer

MAIN_URL = "https://markets.businessinsider.com"
URL_SP500 = "https://markets.businessinsider.com/index/components/s&p_500"


req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?")
dollarRate = float(
    re.search(f"США</\w*><\w*>(\d*\,?\d*)", req.text).group(1).replace(",", ".")
)


class Company:
    def __init__(self, block):
        self.company_block = block
        self.splited_block = self.company_block.text.split()
        self.values = {}
        self.url = f"{MAIN_URL}{self.company_block.find('a')['href']}"
        self.dollar_rate = dollarRate

    def _get_response(self):
        self.response = requests.get(self.url).text

    def _get_company_name_ticker(self):
        self.name = re.findall(r'"label":"([\w\s\\.\(\)\-\&\,\']*)"', self.response)[
            -1
        ].strip()
        self.ticker = re.findall(r'"symbol":"([\w\\.]*)"', self.response)[0]

    def _get_one_year_index(self):
        self.one_year_index = self.splited_block.pop()

    def _get_rub_price(self):
        self.price = round(
            float(re.findall(r'"currentValue":(\d*\.?\d*)', self.response)[-1])
            * self.dollar_rate,
            2,
        )

    def _get_potential_profit(self):
        high_week = float(
            re.search(r"high52weeks:\s*(\d*\.?\d*)", self.response).group(1)
        )
        low_week = float(
            re.search(r"low52weeks:\s*(\d*\.?\d*)", self.response).group(1)
        )
        pot_prof = round(high_week * 100 / low_week - 100, 2)
        self.poten_profit = f"{pot_prof}%"

    def _get_p_e_ratio(self):
        self.p_e_ratio = re.findall(
            r'class="snapshot__data-item">\s*(\-?\d*[\,\.]?\d*\.?\d{,2})', self.response
        )[4].replace(",", "")

    def get_all(self):
        self._get_response()
        self._get_rub_price()
        self._get_company_name_ticker()
        self._get_one_year_index()
        self._get_potential_profit()
        self._get_p_e_ratio()


def get_blocks(main_soap):
    pages_block = main_soap.find("div", attrs={"class": "finando_paging"})
    pages_urls = (f'{URL_SP500}{a["href"]}' for a in pages_block.find_all("a"))
    for url in pages_urls:
        only_table_tags = SoupStrainer("table", attrs={"class": "table table-small"})
        table_block = BeautifulSoup(
            requests.get(url).text, "lxml", parse_only=only_table_tags
        )
        yield from table_block.find_all("tr")[1:]


def get_all_companies():
    main_soup = BeautifulSoup(requests.get(URL_SP500).text, "lxml")
    company_blocks = get_blocks(main_soup)
    return [Company(comp_block) for comp_block in company_blocks]


def get_top_10_prices(all_companies):
    top_10 = sorted(
        all_companies, key=lambda company: float(company.price), reverse=True
    )[:10]
    top_10 = [
        {"code": comp.ticker, "name": comp.name, "price": comp.price} for comp in top_10
    ]
    return top_10


def get_top_10_low_p_e(all_companies):
    top_10 = sorted(
        all_companies, key=lambda company: float(company.p_e_ratio), reverse=False
    )[:10]
    return [
        {"code": comp.ticker, "name": comp.name, "P/E": comp.p_e_ratio}
        for comp in top_10
    ]


def get_top_10_grown(all_companies):
    top_10 = sorted(
        all_companies,
        key=lambda company: float(company.one_year_index.strip("\%")),
        reverse=True,
    )[:10]
    return [
        {"code": comp.ticker, "name": comp.name, "growth": comp.one_year_index}
        for comp in top_10
    ]


def get_top_10_potential(all_companies):
    top_10 = sorted(
        all_companies,
        key=lambda company: float(company.poten_profit.strip("\%")),
        reverse=True,
    )[:10]
    return [
        {"code": comp.ticker, "name": comp.name, "potential profit": comp.poten_profit}
        for comp in top_10
    ]


def write_json(file_name, data):
    with open(
        f"{os.path.join(os.getcwd(), os.path.dirname(__file__), file_name)}.json", "w"
    ) as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    START = datetime.now()

    companies = get_all_companies()

    with ThreadPoolExecutor(max_workers=4) as executor:
        for company in companies:
            executor.submit(company.get_all)

    top_10_prices = get_top_10_prices(companies)
    write_json("top_10_prices", top_10_prices)

    top_10_low_p_e = get_top_10_low_p_e(companies)
    write_json("top_10_low_p_e", top_10_low_p_e)

    top_10_grown = get_top_10_grown(companies)
    write_json("top_10_grown", top_10_grown)

    top_10_potential = get_top_10_potential(companies)
    write_json("top_10_potential", top_10_potential)

    print(f"Program duration = {datetime.now() - START}")
