import requests
import json
import sqlite3


def convert_money():
    amount, fro = input("Enter the amount (indicate the currency,"
                        " for example: 10 GEL ): ").split()
    to = input("Indicate in which currency you want to convert (for example: USD )): ")

    key = "oBaOppeR9zTV8rprHfnLIz8kOeoUfBjW"

    url = f"https://api.apilayer.com/currency_data/" \
          f"convert?to={to}" \
          f"&from={fro}" \
          f"&amount={amount}" \
          f"&apikey={key}"

    response = requests.get(url)

    with open('currency.json', 'w') as file:
        json.dump(json.loads(response.text), file, indent=4)

    dic_jso = response.json()

    print(f"1 {dic_jso['query']['from']} "
          f"= {round(dic_jso['info']['quote'], 2)} {dic_jso['query']['to']}")

    print(f"{dic_jso['query']['amount']} {dic_jso['query']['from']} "
          f"= {round(dic_jso['result'], 1)} {dic_jso['query']['to']}")


def convert_all_currency():
    source = input("Specify the preferred currency (for example: USD ): ")

    key = "oBaOppeR9zTV8rprHfnLIz8kOeoUfBjW"

    url = f""" https://api.apilayer.com/currency_data/live?
               source={source}
               &apikey={key}"""

    response = requests.get(url)

    dic_jes = response.json()

    conn = sqlite3.connect('currency.sqlite')
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS currency  
                       (currency VARCHAR(10),
                        amount FLOAT(10)) """)
    # A specific currency will be recorded against another currency
    for key, value in dic_jes['quotes'].items():
        cursor.execute("INSERT INTO currency (currency, amount) VALUES (?, ?) ", (key, round(value, 2)))
        conn.commit()

    print("Information successfully saved")


def main():
    operation = int(input("Convert money to another currency (1) or \n"
                    "price one currency to another currency (2) : "))
    if operation == 1:
        convert_money()
    else:
        convert_all_currency()


main()
