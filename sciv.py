import argparse
import re
from git import Repo
from tqdm import tqdm

# Regular expression to match import statements
import_regex = r"// File: (.*?)\n(.*?)(?=// File: |$)"

verbose = False

def fetch_openzeppelin_code(contract_path, tag):
    try:
        # Replace "@openzeppelin" with "contracts" in the path
        contract_path = contract_path.replace("@openzeppelin/", "")

        # Get the blob (file) from the repository
        blob = repo.git.show(f"{tag}:{contract_path}")
        return blob
    except:
        # The file does not exist in this version
        return None

def compare_code(imported_code, original_code):
    # Regular expressions to match single and multiline comments, pragma and import statements
    single_comment_regex = r"//.*"
    multi_comment_regex = r"/\*.*?\*/"
    pragma_regex = r"pragma solidity .*?;"
    import_regex = r"import .*?;"

    # Remove comments, pragma and import statements
    imported_code = re.sub(single_comment_regex, "", imported_code, flags=re.MULTILINE)
    imported_code = re.sub(multi_comment_regex, "", imported_code, flags=re.DOTALL)
    imported_code = re.sub(pragma_regex, "", imported_code, flags=re.MULTILINE)
    imported_code = re.sub(import_regex, "", imported_code, flags=re.MULTILINE)
    original_code = re.sub(single_comment_regex, "", original_code, flags=re.MULTILINE)
    original_code = re.sub(multi_comment_regex, "", original_code, flags=re.DOTALL)
    original_code = re.sub(pragma_regex, "", original_code, flags=re.MULTILINE)
    original_code = re.sub(import_regex, "", original_code, flags=re.MULTILINE)

    # Remove leading/trailing white space, normalize line endings, and remove empty lines
    imported_code = "\n".join(line.strip() for line in imported_code.split("\n") if line.strip())
    original_code = "\n".join(line.strip() for line in original_code.split("\n") if line.strip())

    if verbose:
        print("imported code: " + imported_code)
        print("original code: " + original_code)
        print()
        print("---------------------------------------------------------------------------------------------------------------------------")
        print()

    return imported_code == original_code

def check_solidity_file(solidity_file):
    # Read the solidity file
    with open(solidity_file, 'r') as f:
        solidity_code = f.read()

    # Extract all import statements
    imports = re.findall(import_regex, solidity_code, re.DOTALL)

    print("Number of files: " + str(len(imports)))

    matched_contracts = []
    unmatched_contracts = []

    for contract_path, imported_code in tqdm(imports):
        for tag in repo.tags:
            original_code = fetch_openzeppelin_code(contract_path, tag)
            if original_code is not None and compare_code(imported_code, original_code):
                matched_contracts.append((contract_path, str(tag)))
                break
        else:
            unmatched_contracts.append(contract_path)

    print("\n\nMatched contracts:")
    for contract_path, tag in matched_contracts:
        print(f"{contract_path} (version {tag})")

    print("\nUnmatched contracts:")
    for contract_path in unmatched_contracts:
        print(contract_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check a Solidity file against the OpenZeppelin library.')
    parser.add_argument('solidity_file', type=str, help='The path to the Solidity file to check.')
    parser.add_argument('repo_path', type=str, help='The path to the local OpenZeppelin repository.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging.')

    args = parser.parse_args()

    verbose = args.verbose

    repo = Repo(args.repo_path)

    check_solidity_file(args.solidity_file)
