import matplotlib.pyplot as plt

from consts import pools
from interest import get_historical_rates
from main import address


def plot_data(data):
    # Check if data is empty
    if not data:
        print("No data to plot.")
        return

    plt.figure(figsize=(10, 6))

    # Plotting the data
    plt.plot(data, marker='o')  # You can customize the plot with different markers, colors, etc.

    # Adding title and labels
    plt.title('Data Plot')
    plt.xlabel('Index')
    plt.ylabel('Value')

    # Show the plot
    plt.show()


# Example usage
data = get_historical_rates(pools[1], address)["projected_lender_apy"]

def downsample_array(arr, group_size=12):
    # Adjust the length of the array to be divisible by group_size
    adjusted_length = len(arr) - (len(arr) % group_size)
    adjusted_arr = arr[:adjusted_length]

    # Using list comprehension to calculate the average for each group
    downsampled = [sum(adjusted_arr[i:i + group_size]) / group_size for i in range(0, adjusted_length, group_size)]

    return downsampled

# Example usage
downsampled_array = downsample_array(data[100:])
print(downsampled_array)  # This will print the downsampled array


plot_data(downsampled_array)
