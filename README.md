# Smart Contract Import Validator (SCIV)
The **Smart Contract Import Validator (SCIV)** is a simple Python script designed to help Solidity developers and auditors verify the integrity of imported contracts within third-party or foreign smart contracts. The tool ensures that the Solidity files claiming to import well-known libraries, such as OpenZeppelin contracts, have not been tampered with or modified in malicious ways. This can prevent scenarios where a contract might falsely present itself as using a secure, standard implementation while actually containing vulnerabilities.

The tool is particularly useful for identifying instances where a contract has been altered to introduce bugs or backdoors, yet falsely claims to use standard OpenZeppelin implementations.

## Setup
- Install Python 3 if not present already.
- Clone the OpenZeppelin Contracts repository.
- Install the required Python packages: `pip install gitpython tqdm`

## Usage
You can run the tool from the command line with the following syntax:

```
python sciv.py <solidity_file> <repo_path> [-v]
```

- <solidity_file>: The path to the Solidity .sol file that you want to check for tampering.
- <repo_path>: The relative or absolute path to the local clone of the OpenZeppelin repository.
- -v or --verbose: (Optional) Enables verbose logging for detailed output.

## Output
The tool tries to automatically find the referenced smart contract in your checked out repository with known, safe contracts. It lists all automatically matched contracts as well as all contracts which couldn't be automatically matched and need to be checked manually.

Sample usage:
``` shell
$ python3 sciv.py ./SOW.sol ./openzeppelin-contracts/
Number of files: 8
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8/8 [00:01<00:00,  5.38it/s]


Matched contracts:
@openzeppelin/contracts/utils/math/SafeMath.sol (version v4.2.0)
@openzeppelin/contracts/utils/Context.sol (version v4.2.0)
@openzeppelin/contracts/access/Ownable.sol (version v4.7.0)
@openzeppelin/contracts/token/ERC20/IERC20.sol (version v4.6.0)
@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol (version v4.1.0)
@openzeppelin/contracts/token/ERC20/ERC20.sol (version v4.8.0)
@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol (version v4.5.0)

Unmatched contracts:
contracts/SOW.sol
```