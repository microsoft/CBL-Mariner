import argparse
import json
from pathlib import Path
import sys
from types import SimpleNamespace

# Expected Schema:
# class LicenseCollection:
#     header: str
#     table_headers: List[str]
#     licenses: List[License]
#
# class License:
#     origin: str
#     description: str
#     specs: List[str]

def generate_markdown(license_collection):
    res = []
    res.append(license_collection.header)
    res.append('')
    res.append('| ' + ' | '.join(license_collection.table_headers) + ' |')
    res.append('|' + '|'.join([' --- ' for _ in license_collection.table_headers]) + '|')

    for license in license_collection.licenses:
        license.specs.sort(key=str.lower)
        res.append('| {0} | {1} | {2} |'.format(license.origin, license.description, ' <br> '.join(license.specs)))
    
    return '\n'.join(res) + '\n'


def deserialize_json(json_file):
    return json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))


def get_missing_specs(spec_directories, license_collection):
    specs_in_json = set()
    for license in license_collection.licenses:
        for spec in license.specs:
            specs_in_json.add(spec)
    
    specs_in_dir = set()
    for directory in spec_directories:
        specs_in_dir = specs_in_dir.union({f.stem for f in directory.glob('**/*.spec')})

    specs_not_in_json = specs_in_dir - specs_in_json 
    specs_not_in_dir =  specs_in_json - specs_in_dir
    return specs_not_in_json, specs_not_in_dir


def main(input_filename, output_filename, spec_directories):
    with open(input_filename, 'r') as input_file:
        license_collection = deserialize_json(input_file)

    specs_not_in_json, specs_not_in_dir = get_missing_specs(spec_directories, license_collection)

    with open(output_filename, 'w') as output_file:
        output_file.write(generate_markdown(license_collection))

    if len(specs_not_in_json) or len(specs_not_in_dir):
        if len(specs_not_in_json):
            print("Specs present in spec directories that are not present in data file:")
            for s in sorted(specs_not_in_json, key=str.lower):
                print('\t'+ s)
            print()

        if len(specs_not_in_dir):
            print("Specs present in data file that are not present in spec directories:")
            for s in sorted(specs_not_in_dir, key=str.lower):
                print('\t' + s)
            print()

        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=Path)
    parser.add_argument('output_filename', type=Path)
    parser.add_argument('spec_directories', type=Path, nargs='*')
    p = parser.parse_args()
    main(p.input_filename, p.output_filename, p.spec_directories)
