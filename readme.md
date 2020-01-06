# PegTrader

A python library to interact with pegnetd and automate trading on pegnet. Requires pegnetd to be installed.

Offers additional functionality such as limit conversions and the ability to keep retrying conversions until the 
full order has been filled.

You need various processes running in the background: pegnetd, factomd and factom-walletd.

To use public nodes instead you can modify your `~/.pegnetd/pegnetd-conf.toml` file with the following values:

Factomd Open Node - https://api.factomd.net/v2
 
Pegnetd Open Node - https://api.pegnetd.com

### Install

##### Pip:

```
pip install --upgrade git+https://github.com/kompendium-llc/pegtrader.git
```

### Usage

```python
from pegtrader import *

ec = "EC2qxYZgNR6iGTzmXwA9wVFeRov9frY1HSt4MgjJqZ1uwmCoU4RZ"
fct = "FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean"
fct2 = "FA2uPy1H4GqbSynRGjbSSbKKwj7nkBn35sod7s6gBgCy9eMyEfnq"

# Get the current rates for the latest block, print out PEG/USD
rates = current_rates()
print(rates["PEG"])

# Check a transaction (will have to wait until the next block)
entryhash = "a089648ae342466d28ddc846df0cab9479b83dc1b55adcbd98c759f852451bb7"
print(get_txs(entryhash))

# Get all balances for an address
print(balances("FA2J9xMbmp1FbfuzNWCmUNKy714P6yWF9cf7BtK2Fp5F4cRMVUbj"))

# Convert between assets
(entryhash, commit) = newcvt(ec, fct, "PEG", 10, "pUSD")

# Make a transaction
(entryhash, commit) = newtx(ec, fct2 , "PEG", 1000, fct)
print(entryhash)
print(commit)

# Keep trying to convert 10 pUSD into PEG until the full amount has been converted
print(cvt_all("ec", "fct", "pUSD", 10, "PEG", 0))

# Keep trying to convert 10 pUSD into PEG until either 8 attempts have been made or the full amount is converted
print(cvt_all("ec", "fct", "pUSD", 10, "PEG", 8))

# Using the Trader Object

account = Trader("ec", "fct")

# Converts 200 PEG to pBTC only when has reached above 0.01
print(account.dest_limit_cvt(False, 0.01, "PEG", 200, "pBTC"))

# Converts 1 pBTC to pFCT only when it goes below 5000
print(account.src_limit_cvt(True, 5000, "pBTC", 1, "pFCT"))

# Get balances
print(account.balances())
``` 

## Contributing
PR's welcome. Fork the library, create a feature branch and submit it to dev branch here. 
By contributing to this library you agree to it being Apache 2.0 licensed 

#### Donations
FCT: `FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean`

BTC: `bc1qt0hcaf3w7mgms37zj4jdtaas42vpg9uhdwvm5e4tf2maj6yk6etqjdqqpg`

