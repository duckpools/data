from consts import pools
from interest import get_historical_rates



# Example, switch pool index for different pool
address = pools[1]["child"]
print(get_historical_rates(pools[1], address))

