# Technical review, week of 2026-11-02

Source: data/technical_scan.json (created 2026-10-27 1:20 PM New York, market open, so the last bar is still moving). Minimum reward to risk from config is 2.0.

Important note: with the scan's own suggested targets, no stock in either sector reaches 2.0. The scan's reward_risk is measured from the middle of the buy zone. For each pick I moved the target up to the 1.272 Fibonacci extension, a level shown in the file, which is the only change. Entry and stop are the scan's own levels. The reward_risk values below are the same formula rerun with the new target (target minus zone middle, divided by zone middle minus stop). Treat them as my adjustment, not a script output.

## Health Care

| Ticker | Score | RSI | MACD vs signal | Trend |
|---|---|---|---|---|
| GILD | 82.0 | 60.66 | 2.79 above 2.29, histogram not rising | Up (above 50d 149.32 and 200d 137.95) |
| REGN | 79.5 | 59.49 | 9.85 above 3.97, histogram not rising | Up (above 50d 791.54 and 200d 734.86) |
| AMGN | 77.0 | 64.58 | 9.98 above 7.46, histogram not rising | Up (above 50d 418.27 and 200d 369.79) |
| ISRG | 76.7 | 65.22 | 13.96 above 12.36, histogram rising | Fibonacci trend down (dropped) |
| VRTX | 73.7 | 50.85 | 0.92 above -1.38... see note, histogram not rising | Price 515.8 below 50d 522.95, above 200d 477.87 |

Dropped: ISRG (down Fibonacci trend, scan reward_risk 0.73).

**Pick: REGN** (price 810.2)
- Buy zone: entry_low 795.97 (0.236 retracement) to entry_high 810.2 (current price)
- Target: 932.37 (1.272 extension, instead of the scan's 859.34 swing high)
- Stop: 749.2 (scan level)
- Reward to risk: 2.4 with the adjusted target (scan's own: 1.04)
- Runner-up: VRTX. Zone 503.72 (0.382) to 515.8, target 600.5 (1.272 extension), stop 481.4, reward to risk 3.2 adjusted (scan's own: 1.78).

Reasoning: REGN has a full uptrend, RSI in the 50-70 sweet spot, and MACD well above its signal line. Price sits just above the 0.236 level at 795.97, so a pullback to that line gives a close entry. The scan's swing-high target gives too little upside, so I used the 1.272 extension. GILD scores higher but is near its swing high (160.51), and even with the extension its reward to risk is 1.56, which fails. VRTX sits closer to a deeper support but its price is under the 50-day average and its momentum is the weakest of the five, so it is the backup.

## Technology

| Ticker | Score | RSI | MACD vs signal | Trend |
|---|---|---|---|---|
| PANW | 88.7 | 58.8 | -0.13 below -0.72... see note, histogram rising | Up (above 50d 371.03 and 200d 266.97) |
| PLTR | 80.5 | 56.73 | 4.02 below 4.93, histogram rising | Up (above 50d 185.79 and 200d 153.37) |
| CRWD | 79.6 | 60.47 | 2.75 below 2.81, histogram rising | Up (above 50d 236.79 and 200d 165.1) |
| WDAY | 79.4 | 61.14 | 5.04 above 3.18, histogram not rising | Up (above 50d 193.85 and 200d 155.63) |
| QCOM | 78.6 | 53.71 | -0.62 above -0.81, histogram rising | Fibonacci trend down (dropped) |

Dropped: QCOM (down Fibonacci trend, scan reward_risk 0.71).

**Pick: WDAY** (price 205.76)
- Buy zone: entry_low 200.12 (0.236 retracement) to entry_high 205.76 (current price)
- Target: 259.04 (1.272 extension, instead of the scan's 227.49 swing high)
- Stop: 181.35 (scan level)
- Reward to risk: 2.6 with the adjusted target (scan's own: 1.14)
- Runner-up: PLTR. Zone 187.79 (0.236) to 199.63, target 241.93 (1.272 extension), stop 170.51, reward to risk 2.08 adjusted (scan's own: 0.83). Thin margin.

Reasoning: WDAY has a full uptrend, RSI at 61.14, and MACD above its signal line, the only one in the group with that. Price is within 3% of the 0.236 level, so the entry is close to support. PANW scores highest but price (403.25) is far above its nearest support (371.15), and its MACD is below signal. PLTR and CRWD have MACD under signal, and CRWD's adjusted reward to risk is 1.97, under 2.0.

## Cautions
- All figures are from an intraday bar and can change at the close.
- Extension targets are less certain than swing-high targets, since price has not been there recently.
- Research for my own decisions, not financial advice.
