from pegtrader import *

ec = "<YOUR ENTRY CREDIT ADDRESS HERE>"
fct = "<YOUR FACTOM ADDRESS HERE>"

# Create the trader object
account = Trader(ec, fct)

# Whether or not to trigger above or below the limit set
below_limit = True

# Limit price to trigger conversion
limit_price = 6000

# Amount to convert
amount = 0.1

# Source Asset
source = "pBTC"

# Destination Asset
destination = "pFCT"

# Conversion happens here
# Convert 0.1 pBTC to pFCT when the price of pBTC goes below $6000
account.src_limit_cvt(below_limit, limit_price, source, amount, destination)