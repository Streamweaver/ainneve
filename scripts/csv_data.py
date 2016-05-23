import csv
from django.utils.text import slugify

def parse_skills():
    """
    Parses skill csv files into python data dict string to paste into
    a python file later.

    :return: None
    """
    output = ""
    with open('Skills.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, restval=None)
        for row in reader:
            try:
                row["key"] = slugify(row["name"].lower())
                output += """
                "{}": {\n
                    "name": {},\n
                    "trait": {},\n
                    "desc": {},\n
                    "initial": {}\n
                },\n
                """.format(
                    row["key"],
                    row["name"].title(),
                    row["trait"].upper(),
                    row["initial"]
                )
            except KeyError:
                print("*****", row, "*********")
    print(output)


if __name__ == "__main__":
    parse_skills()