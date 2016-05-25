import csv, argparse, string

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
            modify_weapon(row)
            output += """
    {} = {{
        'name': '{}',
        'aliases': {},
        'typeclass': '{}',
        'desc': '{}',
        'weight': {},
        'value': {},
        'damage': {},
        'wear': {},
        'durability': {},
        'bonus': {},
        'use_skill': '{}',
        'fix_skill': '{}',
            }}
            """.format(
                row['key'],
                row['name'],
                row['aliases'],
                row['typeclass'],
                row['desc'],
                row['weight'],
                row['value'],
                row['damage'],
                row['wear'],
                row['durability'],
                row['bonus'],
                row['use_skill'],
                row['fix_skill']
            )
        print(output)

def modify_weapon(row):
    """
    Does some modification of weapon names and aliases to spice them up.

    :param row: dict of weapon data
    """
    # turn aliases into a list.
    aliases = [] if not row['aliases'] else row['aliases'].split(',')

    # Put some jazz on the names.
    if row['model']:
        model  = "%s%s" % (row["model"].upper(), row["damage"])
        if int(row['bonus']) > 0:
            model = "%s%s" % (model, string.ascii_lowercase[int(row["bonus"])])
        row['name'] = "%s %s" % (model, row['name'].title())
        aliases.append(model.lower())

    row['aliases'] = aliases
    row['key'] = row['name'].replace(" ", "_").lower().upper()


if __name__ == "__main__":
    parse_functions = {
        "skills": parse_skills,
        "weapons": parse_weapons,
    }
    parser = argparse.ArgumentParser()
    type_options = "|".join([k for k in parse_functions.keys()])
    help_text = "Type of csv to parse. [%s]" % type_options
    parser.add_argument("type",
                        help=help_text)
    args = parser.parse_args()

    if args.type in parse_functions:
        func = parse_functions[args.type]
        func()
    else:
        print("'%s' is not a valid option.\n" % args.type)
        print(help_text)