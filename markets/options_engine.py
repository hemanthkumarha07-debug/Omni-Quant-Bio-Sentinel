import numpy as np
from scipy.stats import norm

class OptionsGreeks:
    """Calculates the Greeks using the Black-Scholes model."""
    @staticmethod
    def calculate_greeks(S, K, T, r, sigma):
        # S: Stock Price, K: Strike, T: Time (yrs), r: Risk-free, sigma: Volatility
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
        
        return {
            "delta": round(delta, 3),
            "gamma": round(gamma, 4),
            "theta": round(theta, 2)
        }