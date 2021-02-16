import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def plot_cdf(arr):
    arr = sorted(arr)
    mean, std = np.mean(arr), np.std(arr)
    print('mean:', mean, 'std:', std)
    cdf = norm.cdf(arr, mean, std)
    print('cdf:', cdf)
    plt.plot(arr,cdf,label="cdf")
    plt.xlabel("Prices")
    plt.ylabel("Probability")
    plt.title("CDF for continuous distribution")
    plt.legend()
    #plt.show()
    plt.savefig('plot.png')


if __name__=='__main__':
    test_prices = np.array([x*100 for x in range(1,11)])
    plot_cdf(test_prices)
