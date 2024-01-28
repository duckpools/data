from consts import pools
from interest import get_historical_rates



# Example, switch pool index for different pool
address = pools[0]["child"]
print(get_historical_rates(pools[0], address))
