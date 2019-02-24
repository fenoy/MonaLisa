import random
import matplotlib.pyplot as plt

def int_truncated_gauss(mu, sigma, limit):
    while True:
        output = int(random.gauss(mu, sigma))
        if limit[0] <= output <= limit[1]: break
    return output

def randmut(mu, sigma, limit):
    low_limit = max(limit[0], int(mu-sigma))
    high_limit = min(limit[1], int(mu+sigma))
    return random.randint(low_limit, high_limit)
