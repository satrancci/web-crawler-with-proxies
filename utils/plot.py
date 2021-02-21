import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

DIR_WRITE = './plots'

def plot_single_cdf(city, prices):
    if not city or not prices: 
        raise ValueError(f"[PLOT_SINGLE_CDF]: One (or both) of the arguments is missing")
    #print(f"[PLOT_SINGLE_CDF]: city: {city}")
    prices = sorted(prices)
    mean, std = np.mean(prices), np.std(prices)
    cdf = norm.cdf(prices, mean, std)
    plt.clf()
    plt.plot(prices,cdf,label=f"{city} (n={len(prices)})")
    plt.xlabel("Prices")
    plt.ylabel("Probability")
    plt.title("CDF for continuous distribution")
    plt.legend()
    #plt.show()
    plt.savefig(f"{DIR_WRITE}/{city}_cdf_plot.png")


def plot_multiple_cdf(cities_to_prices):
    '''
    cities_to_prices: defaultdict(list) with CITY as key and PRICES as value.
    '''
    N = sum(map(lambda x: len(x), cities_to_prices.values()))
    plt.xlabel("Prices")
    plt.ylabel("Probability")
    plt.title(f"CDF for continuous distribution (N={N})")

    for city, prices in cities_to_prices.items():
        prices = sorted(prices)
        mean, std = np.mean(prices), np.std(prices)
        cdf = norm.cdf(prices, mean, std)
        plt.plot(prices,cdf,label=f"{city} (n={len(prices)})")
        plt.legend()


    #plt.show()
    plt.savefig(f"{DIR_WRITE}/all_cities_cdf_plot.png")


