import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


if __name__=='__main__':

    test_prices = np.array([x*100 for x in range(1,11)])
    mean, std = np.mean(test_prices), np.std(test_prices)
    cdf = norm.cdf(test_prices, mean, std)
    plt.plot(test_prices,cdf,label="cdf")
    plt.xlabel("Prices")
    plt.ylabel("Probability")
    plt.title("CDF for continuous distribution")
    plt.legend()
    #plt.show()
    plt.savefig('plot.png')