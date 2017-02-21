#!/usr/bin/env python3

import sqlite3
from argparse import ArgumentParser
from decimal import Decimal
from pathlib import Path
from pprint import pprint

import requests
from bs4 import BeautifulSoup

connection = sqlite3.connect("currency_conversions_sqlite.db")
connection.execute("CREATE TABLE IF NOT EXISTS conversions (currency TEXT UNIQUE, usd NUMERIC)")


def populate_conversion_table(conversion_xml):
    soup = BeautifulSoup(conversion_xml, "lxml")
    connection.execute("DELETE FROM conversions")
    for conversion in soup.select("response conversion"):
        currency = conversion.select("currency")[0].string
        rate = float(conversion.select("rate")[0].string)
        connection.execute("INSERT INTO conversions VALUES (?, ?)", [currency, rate])


def get_conversions():
    return dict(connection.execute("SELECT currency, usd FROM conversions"))


def currency_amounts_from_arg(currency_arg):
    if len(currency_arg) % 2 != 0:
        raise ValueError("Invalid foreign_currency arg: {}".format(currency_arg))
    result = []
    for i in range(0, len(currency_arg), 2):
        result.append("{} {}".format(currency_arg[i], currency_arg[i + 1]))
    return result


def convert_currency(amount_str):
    currency_type, amount = amount_str.split(" ")
    amount = float(amount)
    return "USD {:.2f}".format(get_conversions()[currency_type.upper()] * amount)


def show_conversions(amount_strings):
    for amount_str in amount_strings:
        print("{} = {}".format(amount_str.upper(), convert_currency(amount_str)))


if __name__ == "__main__":
    # xml = requests.get("https://wikitech.wikimedia.org/wiki/Fundraising/tech/Currency_conversion_sample?ctype=text/xml&action=raw").text
    xml = Path("conversions.xml").read_text()
    populate_conversion_table(xml)

    parser = ArgumentParser(
        description="Convert foreign currencies to and from US dollars.")
    parser.add_argument(
        "foreign_currency", nargs="+",
        help="Convert from foreign currencies to US dollars.")
    args = parser.parse_args()
    show_conversions(currency_amounts_from_arg(args.foreign_currency))
