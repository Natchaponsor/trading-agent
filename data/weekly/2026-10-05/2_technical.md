# Technical review, week of 2026-10-05

Source: data/technical_scan.json (created 2026-10-04, newer than data/sectors_selected.json). min_reward_risk = 2.0.
Reward_risk convention (checked against the file): (target - midpoint of entry zone) / (midpoint - stop).
Note: no stock in either sector passes 2.0 on the file's own suggested_levels (best: NVDA 1.58, GILD 1.56). Picks below use alternative levels that appear in the file (extensions, swing high); the adjusted reward_risk is my computation from those file prices.

## Technology

| Ticker | Score | RSI | MACD vs signal | Trend (price > 50d > 200d) | Fib trend | Suggested R/R |
|---|---|---|---|---|---|---|
| LITE | 92.1 | 66.68 | 37.16 > 24.32, hist rising | healthy (1085.42 > 879.03 > 745.43) | up | 1.44 |
| MSFT | 90.4 | 62.7 | 7.88 > 7.55, hist rising | healthy (517.53 > 487.39 > 431.46) | up | 1.47 |
| SHOP | 89.9 | 61.14 | 2.67 > 1.01, hist rising | healthy (151.39 > 140.75 > 129.55) | up | 0.77 |
| NVDA | 89.1 | 63.01 | 3.54 > 2.72, hist rising | healthy (233.95 > 218.12 > 200.38) | up | 1.58 |
| LRCX | 87.7 | 67.76 | 7.84 > 1.4, hist rising | healthy (347.49 > 305.78 > 274.61) | up | 1.23 |

**Pick: NVDA** (price 233.95)
- entry_low 222.63 (Fib 0.236), entry_high 233.95 (current price)
- target 277.81 (Fib extension 1.618) ; stop 211.06 (suggested stop from file)
- reward_risk 2.87 (adjusted; the file's 1.272 target of 255.46 gives only 1.58)

**Runner-up: MSFT** (price 517.53): entry 481.71 (Fib 0.236) to 517.53, target 630.57 (extension 1.618), stop 451.70, reward_risk 2.73 on those adjusted levels (file suggests 1.47).

Reasoning: All five are in clean uptrends with RSI in the 50-70 band and improving MACD, so the choice comes down to risk. SHOP fails outright (target equals swing high, 0.77) and LRCX is the weakest at 1.23 after a big pullback from its 438.03 high. NVDA sits closest to a Fibonacci support (price about 4.8% above the 0.236 level at 222.63, versus MSFT about 7% and LITE about 11%), which gives the tightest stop. The 2.0 threshold is only met by using the 1.618 extension, so the target is ambitious; if only the 1.272 target is accepted, NVDA does not qualify (1.58). MSFT is nearly as clean but further from support.

## Health Care

| Ticker | Score | RSI | MACD vs signal | Trend | Fib trend | Suggested R/R |
|---|---|---|---|---|---|---|
| AMGN | 66.2 | 47.84 | 1.2 > -0.34, hist not rising | price 403.04 < 50d 408.54, > 200d 360.98 | up | 0.72 |
| GILD | 65.0 | 44.48 | 1.47 < 2.31, hist not rising | price 144.74 > 50d 142.63 > 200d 135.22 | up | 1.56 |
| DXCM | 54.2 | 43.7 | -0.04 < 0.32, hist not rising | price 85.36 < 50d 86.38, > 200d 73.05 | up | 1.18 |
| REGN | 49.2 | 34.91 | -11.59 < -3.49, hist not rising | price 735.2 < 50d 784.56, about at 200d 734.54 | up | 1.51 |
| ISRG | 42.8 | 51.21 | 7.45 > 6.59, hist not rising | price 391.95 > 50d 380.04, < 200d 447.22 | down (dropped) | 0.66 |

**Pick: GILD** (price 144.74)
- entry_low 141.11 (Fib 0.382), entry_high 144.74 (current price)
- target 163.52 (Fib extension 1.272) ; stop 135.69 (suggested stop from file)
- reward_risk 2.85 (adjusted; file's target 154.2 swing high gives 1.56)

**Runner-up: DXCM** (price 85.36): entry 84.12 (Fib 0.236) to 85.36, target 102.35 (extension 1.272), stop 78.10, reward_risk 2.65 adjusted (file suggests 1.18). Weaker: RSI 43.7, MACD below signal, below 50-day.

Reasoning: The sector is technically weak. ISRG is dropped for a down Fibonacci trend, and AMGN (0.72) and DXCM (1.18) fall below the reward_risk floor on file levels. REGN has the worst momentum (RSI 34.91, MACD -11.59) and is sitting on its 200-day, so it is not a safe pick. GILD is the only name still above both moving averages with a decent suggested R/R (1.56) and a buy zone starting at the 0.382 retracement, close to the current price. Its RSI (44.48) and MACD (below signal) are not supportive, so this is a low-conviction pick that needs the target extended beyond the swing high to reach 2.0.
