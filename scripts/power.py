#!/usr/bin/env python3
"""两比例样本估算：python scripts/power.py --baseline 0.04 --mde-to 0.05 [--alpha 0.05 --power 0.8 --consent 0.6]"""
import argparse
from math import sqrt
from statistics import NormalDist

def per_arm(p1, p2, alpha=0.05, power=0.8):
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    n = (za * sqrt(2 * pb * (1 - pb)) + zb * sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
    return int(round(n))

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--baseline", type=float, required=True)
    a.add_argument("--mde-to", type=float, required=True)
    a.add_argument("--alpha", type=float, default=0.05)
    a.add_argument("--power", type=float, default=0.8)
    a.add_argument("--consent", type=float, default=1.0)
    x = a.parse_args()
    n = per_arm(x.baseline, x.mde_to, x.alpha, x.power)
    print(f"每组样本约 {n}；按同意率 {x.consent} 折算所需访客约 {int(round(n / x.consent))}")
