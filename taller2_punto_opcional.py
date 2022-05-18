
import scipy.stats
from scipy import sqrt


def get_thompson_for_n(n):
    alpha = 0.05
    qt = scipy.stats.t.ppf(q = 1 - alpha/2, df = n-2)
    thompson = (qt * (n - 1)) / (sqrt(n) * sqrt(n - 2 + qt**2))
    return thompson

def find_outliers(df):
    outliers = []
    
    while True:
        rtts = df["rtt"]
        df["rtt_deviations"] = abs(rtts - rtts.mean())
        std = rtts.std()
        thompson = get_thompson_for_n(len(df))
        if max(df["rtt_deviations"]) > thompson * std:
            outlier = df.loc[df["rtt_deviations"].idxmax()]

            print("Outlier found.")
            print(outlier)
            outliers.append(outlier)

            df = df.drop(df["rtt_deviations"].idxmax())
        else:
            break
    
    return outliers
