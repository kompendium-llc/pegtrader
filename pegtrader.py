import subprocess
import json
from decimal import *
from time import sleep
# import fire

"""
 You will need various processes running: pegnetd, factomd and factom-walletd
 Can modify the /.pegnetd/pegnetd-conf.toml to use open nodes for use with this library
 Factom Open Node: https://api.factomd.net/v2
 Pegnetd Open Node: https://api.pegnetd.com
"""
CLI = "pegnetd"

class Trader:
    def __init__(self, ecaddress, fctaddress):
        self.ec = ecaddress
        self.fct = fctaddress
        self.dryrun = False

    def balances(self):
        """Returns hashmap of all balances for the Trading Address
        Usage:
        account = Trader("EC2qxYZgNR6iGTzmXwA9wVFeRov9frY1HSt4MgjJqZ1uwmCoU4RZ", "FA2J9xMbmp1FbfuzNWCmUNKy714P6yWF9cf7BtK2Fp5F4cRMVUbj")
        amounts = account.balances()
        print(amounts["pUSD"])
        """
        balances(self.fct)


    def burn(self, amount):
        """
        Returns the txid and burns the specified amount
        Usage:
        account = Trader("EC2qxYZgNR6iGTzmXwA9wVFeRov9frY1HSt4MgjJqZ1uwmCoU4RZ", "FA2J9xMbmp1FbfuzNWCmUNKy714P6yWF9cf7BtK2Fp5F4cRMVUbj")
        txid = account.burn(10)
        print(txid)
        """
        burn(self.fct, (str(Decimal(amount))))

    def newtx(self, token, amount, fctoutput):
        """
        Creates and sends a new tx from the trading account
        returns a tuple with the entryhash and commit respectively.
        Usage:
        account = Trader("EC2qxYZgNR6iGTzmXwA9wVFeRov9frY1HSt4MgjJqZ1uwmCoU4RZ", "FA2J9xMbmp1FbfuzNWCmUNKy714P6yWF9cf7BtK2Fp5F4cRMVUbj")
        (entryhash, commit) = account.newtx("PEG", 120, "FA32xV6SoPBSbAZAVyuiHWwyoMYhnSyMmAHZfK29H8dx7bJXFLja")
        print(entryhash)
        print (commit)
        """
        newtx(self.ec, self.fct, token, str(Decimal(amount)), fctoutput)

    def newcvt(self, src, amount, dest):
        """
        Converts the source asset to the destination asset
        returns a tuple with the entryhash and commit respectively.
        Usage:
        account = Trader("EC2qxYZgNR6iGTzmXwA9wVFeRov9frY1HSt4MgjJqZ1uwmCoU4RZ", "FA2J9xMbmp1FbfuzNWCmUNKy714P6yWF9cf7BtK2Fp5F4cRMVUbj")
        (entryhash, commit) = account.newcvt("pFCT", 12, "pUSD")
        print(entryhash)
        print (commit)
        """
        newcvt(self.ec, self.fct, src, str(Decimal(amount)), dest)


    def src_limit_cvt(self, below, limit, src, amount, dest):
        """Creates a conversion only when the source asset reaches either above or below a certain limit."""
        direction = "below" if below else "above"
        if self.dryrun:
            print("### Dryrun Simulation ###")
        print("Converting From: %s\nAmount: %s\nConverting To: %s" % (src, amount, dest))
        print("Limit Conversion: Waiting for %s rate to be %s %s" % (src, direction, limit))
        waiting = True
        limit = Decimal(limit)
        old_rate = Decimal(0)
        while waiting:
            rate = Decimal(current_rates()[src])
            if rate != old_rate:
                print("Current rate: %s" % str(rate))
                if below:
                    waiting = limit < rate
                else:
                    waiting = limit > rate
            sleep(180)
        if self.dryrun:
            print("Dryrun: Limit condition met. Not submitting Conversion")
            return None
        print("Condition met, submitting conversion...")
        newcvt(self.ec, self.fct, src, str(Decimal(amount)), dest)

    def dest_limit_cvt(self, below, limit, src, amount, dest):
        try:
            if self.dryrun:
                print("### Dryrun Simulation ###")
            direction = "below" if below else "above"
            print("Converting From: %s\nAmount: %s\nConverting To: %s" % (src, amount, dest))
            print("Limit Conversion: Waiting for %s rate to be %s %s" %  (dest, direction, limit))
            waiting = True
            limit = Decimal(limit)
            old_rate = Decimal(0)
            while waiting:
                rate = Decimal(current_rates()[dest])
                if rate != old_rate:
                    print("Current rate: %s" % str(rate))
                    if below:
                        waiting = limit < rate
                    else:
                        waiting = limit > rate
                sleep(180)
            if self.dryrun:
                print("Dryrun: Limit condition met. Not submitting Conversion")
                return None
            print("Limit condition met, submitting conversion.")
            args = [CLI, "newcvt", self.ec, self.fct, src, str(Decimal(amount)), dest]
            result = subprocess.run(args, capture_output=True, check=True)
            details = result.stdout.decode("utf-8").split()
            return details[3], details[5]
        except subprocess.CalledProcessError as e:
            print(e.output)


def balances(address):
    """
    Returns hashmap of all balances for provided address
    Usage:
    amounts = balances("FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean")
    print(amounts["PEG"])
    """
    try:
        args = [CLI, "balances", address]
        result = subprocess.run(args, capture_output=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.output)


def balance(token, address):
    """
    Returns int given the particular balance for an address
    Usage:
    amount = balance("PEG", "FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean")
    print(amount)
    """
    try:
        args = [CLI, "balance", token, address]
        result = subprocess.run(args, capture_output=True, check=True)
        print(result)
        return result.stdout.decode("utf-8").split()[0]
    except subprocess.CalledProcessError as e:
        print(e.output)


def burn(address, amount):
    """
    Returns the txid and burns the specified amount for an address
    Usage:
    txid = burn("FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean", 10)
    print(txid)
    """
    try:
        args = [CLI, "burn", address, (str(Decimal(amount)))]
        result = subprocess.run(args, capture_output=True, check=True)
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)


def newtx(ecaddress, fctinput, token, amount, fctoutput):
    """
    Creates and sends a new tx, returns a tuple with the entryhash and commit respectively.
    Usage:
    (entryhash, commit) = newtx("EC3eX8VxGH64Xv3NFd9g4Y7PxSMnH3EGz5jQQrrQS8VZGnv4JY2K", "FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean",  "PEG", 200, "FA32xV6SoPBSbAZAVyuiHWwyoMYhnSyMmAHZfK29H8dx7bJXFLja")
    print(entryhash)
    print (commit)
    """
    try:
        args = [CLI, "newtx", ecaddress, fctinput, token, str(Decimal(amount)), fctoutput]
        result = subprocess.run(args, capture_output=True, check=True)
        details = result.stdout.decode("utf-8").split()
        return details[3], details[5]
    except subprocess.CalledProcessError as e:
        print(e.output)


def newcvt(ecaddress, fctaddress, src, amount, dest):
    """
    Converts the source asset to the destination asset
    returns a tuple with the entryhash and commit respectively.
    Usage:
    (entryhash, commit) = newcvt("EC3eX8VxGH64Xv3NFd9g4Y7PxSMnH3EGz5jQQrrQS8VZGnv4JY2K", "FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean", "pFCT", 100, "pUSD")
    print(entryhash)
    print (commit)
    """
    try:
        args = [CLI, "newcvt", ecaddress, fctaddress, src, str(Decimal(amount)), dest]
        result = subprocess.run(args, capture_output=True, check=True)
        details = result.stdout.decode("utf-8").split()
        return details
    except subprocess.CalledProcessError as e:
        print(e.output)

def status():
    """
    Gets the current pegnetd syncheight and factomd block height. They should be the same on a fully
    synced node
    Usage:
    print(status())
    """
    try:
        args = [CLI, "status"]
        result = subprocess.run(args, capture_output=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.output)

def get_rates(height):
    """
    You can query the USD rates of each asset for any recorded block with get rates.
    Usage:
    print(get_rates(214297))
    """
    try:
        args = [CLI, "get", "rates", str(height)]
        result = subprocess.run(args, capture_output=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.output)

def get_tx(txid):
    """
    After making a transaction, you will want to confirm it was a valid transaction.
    If you are given a pegnet txid, you can use the get tx cli command to confirm a payment.
    A Factom blockchain explorer is NOT sufficient. Just because a tx was recorded on chain,
    does not mean it is valid and executed. The explorer must specifically support pegnet to
    properly indicate if a tx was executed. If the get tx command returns transaction data,
    that means it was executed.
    Usage:
    print(get_tx("00-64bdda388e7957d038fe01696f67125230bae750506866aa801894ecac3c86bf"))
    """
    try:
        args = [CLI, "get", "tx", txid]
        result = subprocess.run(args, capture_output=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.output)

def get_txs(tx):
    """
    This allows you to grab all transactions for a height, hash, or address.
    Usage:
    # Entryhash
    print(get_txs("8cc6bfd35330f0ae8e71a425a7cd50aec07780ea0f462b345addf0190c1e8803"))
    # Height
    print(get_txs(222222)
    """
    try:
        args    = [CLI, "get", "txs", str(tx)]
        result = subprocess.run(args, capture_output=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.output)

def current_rates():
    """
    Current rates is similar to get rates except it will first get the sync height of pegnetd
    before querying the most recent block
    Usage:
    print(current_rates())
    """
    try:
        height = status()["syncheight"]
        rates = get_rates(height)
        return rates
    except subprocess.CalledProcessError as e:
        print(e.output)


def current_btc_rates():
    """Returns the all current rates in btc"""
    try:
        getcontext().prec = 8
        btc_rates = {}
        rates = current_rates()
        btc = rates["pXBT"]
        for (k, v) in rates.items():
            btc_rates[k] = Decimal(v) / Decimal(btc)
        return btc_rates
    except subprocess.CalledProcessError as e:
        print(e.output)

def custom_rates(base):
    """Custom base for working out conversion rates."""
    try:
        getcontext().prec = 8
        btc_rates = {}
        rates = current_rates()
        btc = rates[base]
        for (k, v) in rates.items():
            btc_rates[k] = Decimal(v) / Decimal(btc)
        return btc_rates
    except subprocess.CalledProcessError as e:
        print(e.output)
    except KeyError:
        print("Base ticker not found: %s" % base)

def custom_rate(quote, base):
    """Custom quote and base for working out conversion rates."""
    try:
        getcontext().prec = 8
        rates = current_rates()
        base = rates[base]
        return Decimal(rates[quote]) / Decimal(base)

    except subprocess.CalledProcessError as e:
        print(e.output)
    except KeyError:
        print("Ticker/s not found: %s/%s" % (quote, base))

def cvt_all(ecaddress, fctaddress, src, amount, dest, retries):
    """
    Continues trying to convert until the either the full amount of number of retries is reached.
    To continue until all is converted set retries value to 0
    Usage:
    print(cvt_all("EC3eX8VxGH64Xv3NFd9g4Y7PxSMnH3EGz5jQQrrQS8VZGnv4JY2K", "FA2dJL4qbQimfkXjP7jREdm48AjPzdS8rcosfJisG2L465bs1ean", "pFCT", 100, "pUSD", 0))
    """
    try:
        src_balance = int(balance(src, fctaddress))
        desired_balance = src_balance - amount
        if desired_balance < 0:
            desired_balance = 0
        retries -= 1
        attempts = 0
        while attempts != retries:
            details = newcvt(ecaddress, fctaddress, src, str(Decimal(amount)), dest)
            print(details)
            new_balance = src_balance
            while src_balance == new_balance:
                sleep(300)
                new_balance = int(balance(src, fctaddress))
            diff = src_balance - new_balance
            print("Converted %s of %s" % (diff, amount))
            amount -= diff
            src_balance = new_balance
            if src_balance < desired_balance:
                print("Completed")
                return True
        return False
    except subprocess.CalledProcessError as e:
        print(e)

# if __name__ == '__main__':
#     fire.Fire(Trader)
