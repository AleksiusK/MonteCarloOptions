import numpy as np
from numpy.random import seed


def paths(S, K, T, r, q, sigma, steps, N):
    """
    Generate possible paths for stock prices as Geometric Brownian motion.

    Inputs
    :param S: Current stock price
    :param K: Strike
    :param T: Time to maturity. 1 year = 1, 1 month = 1/12 = 0.833..
    :param r: Risk free rate
    :param q: dividend yield
    :param sigma: Volatility
    :param steps: Amount of time steps
    :param N: Number of iterations

    Output
    :return: Matrix of paths
    """

    dt = T/steps ##Lenght of on timestep
    st = np.log(S) + np.cumsum(((r-q-(sigma**2)/2)*dt + sigma*np.sqrt(dt) * np.random.normal(size=(steps, N))), axis=0)
    return np.exp(st) ##Prices are lognormal

def main():
    inputs = ["Current stock price", "Strike", "Time to maturity", "Risk free rate", "Dividend yield", "Volatility",
              "Amount of time steps"]
    vars = [] ##Variables
    cres = [] ##Results from call
    pres = [] ##Results from put
    n = 0
    iters = 100000
    ##Error between iterations
    c_err = 100.00
    p_err = 100.00
    while n < 7:
        vars.append(float((input(inputs[n] + ": "))))
        n += 1

    ## Current iteration
    i = 0
    while i <= 100:
        i += 1
        pths = paths((vars[0]), (vars[1]), (vars[2]), (vars[3]), (vars[4]), (vars[5]), int(vars[6]), iters)
        ##The profit at expiration
        call_payoffs = np.maximum(pths[-1] - vars[1], 0)
        put_payoffs = np.maximum(vars[1] - pths[-1], 0)
        ##The mean over all profits in the matrix, discounted to present value
        c = np.mean(call_payoffs)*np.exp(-vars[3]*vars[2])
        cres.append(c)
        p = np.mean(put_payoffs) * np.exp(-vars[3] * vars[2])
        pres.append(p)
        if len(cres) != 0:
            c_err = (sum(cres) / len(cres)) - c
            p_err = (sum(pres) / len(pres)) - p
        del pths
        ##print("Call price, iteration {}: {}".format(i, c))
        ##print("Error: {}".format(c_err))

    c_price = (sum(cres) / len(cres))
    p_price = (sum(pres) / len(pres))
    print("Call price and error: ", c_price, ", ", c_err)
    print("Put price and error: ", p_price, ", ", p_err)


main()