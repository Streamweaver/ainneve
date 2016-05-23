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


if __name__ == "__main__":
    parse_skills()