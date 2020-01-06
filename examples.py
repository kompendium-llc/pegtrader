from pegtrader import *

# Basic Examples
# 
# You'll need to replace these with your own addresses for many of these functions to work
ec = "EC2qxYZgNR6iGTzmXwA9wVFeRov9frY1HSt4MgjJqZ1uwmCoU4RZ"
fct = "FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean"
fct2 = "FA2uPy1H4GqbSynRGjbSSbKKwj7nkBn35sod7s6gBgCy9eMyEfnq"

# Get current rates denominated in pBTC
print(current_btc_rates())

# Get current rates denominated in pETH
print(custom_rates("pETH"))

# Get current rate of PEG/pADA
print(custom_rate("PEG", "pADA"))

# Individually print all rates denominated in pUSD
for (k,v) in current_rates().items():
    print(k, v)

# Burn 1 FCT into PEG
print(burn("fct", 1))

# Send 1 PEG from fct to fct2
print(newtx("ec", "fct", "PEG", 1, "fct2"))

# Convert 1 PEG into pUSD
print(newcvt("ec", "fct", "PEG", 1, "pUSD"))

# Keep trying to convert 10 pUSD into PEG until the full amount has been converted
print(cvt_all("ec", "fct", "pUSD", 10, "PEG", 0))

# Keep trying to convert 10 pUSD into PEG until either 8 attempts have been made or the full amount is converted
print(cvt_all("ec", "fct", "pUSD", 10, "PEG", 8))

# Get tx info
print(get_tx("00-64bdda388e7957d038fe01696f67125230bae750506866aa801894ecac3c86bf"))

# Get txs made
print(get_txs("8cc6bfd35330f0ae8e71a425a7cd50aec07780ea0f462b345addf0190c1e8803"))
balances("fct")
print(balance("PEG", "fct"))


# Trader Object
# Setting dryrun to true when instantiating a Trader object is a good idea.
account = Trader("ec", "fct")
account.dryrun = True

# Converts 200 PEG to pBTC only when has reached above 0.01
print(account.dest_limit_cvt(False, 0.01, "PEG", 200, "pBTC"))

# Converts 1 pBTC to pFCT only when it goes below 5000
print(account.src_limit_cvt(True, 5000, "pBTC", 1, "pFCT"))

# Sends a TX
print(account.newtx("PEG", 1, "fct2"))
