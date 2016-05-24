import csv
from django.utils.text import slugify

def parse_skills():
    """
    Parses skill csv files into python data dict string to paste into
    a python file later.

    :return: None
    """
    output = ""
    with open('Skills.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row:
                output += """
                "{}": {{
                    'name': "{}",
                    "trait": "{}",
                    "desc": "{}",
                    "initial": {}
                }},
                """.format(
                    row["key"].lower(),
                    row["name"].title(),
                    row["trait"].upper(),
                    row["desc"],
                    row["initial"] or "None"
                )
    print(output)

def parse_weapons():
    """
    Parses weapon csv files into a python data dict string to past into python file
    later.

    :return: None

    """
    output = ""
    with open('Weapons.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            aliases = ""
            if row['aliases']:
                aliases = ", ".join("'%s'" % a.strip() for a in row['aliases'].split(','))
            output += """
    {} = {{
        'name': '{}',
        'aliases': [{}],
        'typeclass': '{}',
        'desc': '{}',
        'weight': {},
        'value': {},
        'damage': {},
        'ware': {},
        'bonus': {},
        'use_skill': '{}',
        'fix_skill': '{}',
            }}
            """.format(
                row['key'].upper(),
                row['name'].title(),
                aliases,
                row['typeclass'],
                row['desc'],
                row['weight'],
                row['value'],
                row['damage'],
                row['ware'],
                row['bonus'],
                row['use_skill'],
                row['fix_skill']
            )
        print(output)

if __name__ == "__main__":
    parse_weapons()