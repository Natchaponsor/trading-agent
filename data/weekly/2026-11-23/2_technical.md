# Technical report, week of 2026-11-23

Source: data/technical_scan.json (created 2026-11-22). All prices come from that file. Minimum reward_risk is 2.0.

Important: no stock in either top 5 reaches 2.0 with the script's own suggested_levels (best was 1.8). I kept each suggested buy zone and stop, and moved only the target up to the Fibonacci 1.272 extension, which is shown in the file. The new reward_risk is my own division using the middle of the buy zone, which matches how the script's numbers work out (IDXX 1.0 checks out). The script did not print these new ratios, so please treat them as calculated by me, not script output.

## Health Care

| Ticker | Score | RSI | MACD vs signal | Trend |
|---|---|---|---|---|
| IDXX | 72.5 | 59.78 | below (34.81 vs 38.07) | up (price above 50d and 200d, 50d above 200d) |
| GILD | 70.0 | 54.46 | below (3.23 vs 4.11) | up |
| REGN | 67.5 | 57.52 | below (33.58 vs 37.94) | up |
| GEHC | 65.0 | 56.57 | below (2.93 vs 3.45) | up |
| AMGN | 50.0 | 42.41 | below (3.70 vs 8.55) | up |

Pick: IDXX (Idexx Laboratories), price 676.21
- Buy zone: 663.44 to 676.21 (0.236 retracement up to current price)
- Target: 771.71 (Fibonacci 1.272 extension). Script target was 713.74 (swing high).
- Stop: 626.0 (suggested_levels)
- Reward to risk: about 2.32 (script showed 1.0 with the swing-high target)

Runner-up: GEHC, price 80.64. Buy zone 76.99 to 80.64 (0.382 retracement to price), target 95.08 (1.272 extension), stop 72.99, reward to risk about 2.79 (script showed 1.5).

Reasoning: IDXX has the top score, a clean uptrend, RSI in the healthy range, and the best strength against the Nasdaq-100 (34.62% over 3 months). Price sits about 2% above the 0.236 retracement at 663.44, so the entry is fairly close to support. The weak spot is MACD, which is below its signal line and not rising, so momentum is cooling. The original target was only the swing high, which gave just 1.0 reward to risk, so it needs the extension target to pass the filter. GEHC is a good alternative with a better ratio and a price right at the 0.236 level (81.03), but it scores lower. GILD and REGN scored lower than IDXX. AMGN has weak RSI (42.41).

## Consumer Staples

| Ticker | Score | RSI | MACD vs signal | Trend |
|---|---|---|---|---|
| KHC | 88.0 | 59.32 | above (0.36 vs 0.32), histogram rising | up |
| MDLZ | 72.0 | 56.17 | below (1.05 vs 1.23) | up |
| KDP | 70.0 | 48.66 | below (0.36 vs 0.75) | up |
| CCEP | 68.5 | 57.58 | below (2.39 vs 2.67) | up |
| PEP | 47.3 | 53.24 | below (2.24 vs 2.70) | weak (price above 50d but below 200d at 143.33) |

Pick: KHC (Kraft Heinz), price 25.39
- Buy zone: 25.34 to 25.39 (0.382 retracement up to current price)
- Target: 29.29 (Fibonacci 1.272 extension). Script target was 26.22 (0.236 retracement, below swing high 27.65).
- Stop: 24.39 (suggested_levels)
- Reward to risk: about 4.03 (script showed 0.87)

Runner-up: MDLZ, price 66.28. Buy zone 66.17 to 66.28, target 72.09 (1.272 extension), stop 63.83, reward to risk about 2.45 (script showed 1.12).

Reasoning: KHC is the only stock in either sector with MACD above its signal line and a rising histogram, and it has the highest score by a wide margin. Price is right on the 0.382 retracement (25.34), which allows a close stop. The weak spot is relative strength against the Nasdaq-100, the lowest of the five at 0.4 on the script's scale, and the stock is up only 1.2% over the last month. The 1.272 target is a long way above the swing high of 27.65, so the big ratio depends on KHC breaking to new highs. A more cautious plan would use the swing high of 27.65 as the target. MDLZ is steadier but has a downward MACD cross.

Not financial advice. Research for my own decisions.
