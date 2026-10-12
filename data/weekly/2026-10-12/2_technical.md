# Technical review, week of 2026-10-12

Source: data/technical_scan.json (created 2026-10-12T02:05-04:00), config min_reward_risk = 2.0. All prices are from that file. reward_risk below is the scan's figure on its suggested_levels.

## Technology

| Ticker | Score | RSI | MACD vs signal | Trend (Fib) | Scan reward_risk |
|---|---|---|---|---|---|
| MSFT | 90.8 | 67.52 | 10.69 > 9.2 | up, above 50d/200d | 1.4 |
| GOOG | 87.2 | 55.97 | 1.19 > 0.24 | up | 0.61 |
| TRI | 85.7 | 56.85 | -0.1 < -0.68? no: -0.1 > -0.68 (both negative) | up | 1.56 |
| LITE | 83.2 | 62.6 | 54.91 > 43.48 | up | 0.63 |
| ADI | 83.1 | 60.54 | 10.67 > 9.21 | up | 0.84 |

**Pick: NONE.** Every top-5 name has reward_risk below 2.0 on the scan's suggested_levels, so all are dropped under the rules.

Closest: MSFT (reward_risk 1.4; entry 492.69-535.07, target 588.54, stop 460.49). It is at its swing high (537.22), price 535.07, so it is extended with little room above entry.
Runner-up / watch: MSFT. Using only levels in the file, a pullback entry at 492.69 (0.236 retracement) with the same target 588.54 and stop 460.49 would give about (588.54-492.69)/(492.69-460.49) = 2.98. This is a conditional alternative, not a current buy zone; price is 535.07 now. Alternatively target 653.82 (1.618 extension) from entry_high 535.07 gives about 1.59, still under 2.0.

Reasoning: Technology is strong on trend and momentum, but the best names are at or near swing highs, so a stop at a retracement level is far away and the upside to the next extension is small. Nothing offers a close-in Fibonacci support with at least 2:1. Wait for a pullback rather than chase.

## Health Care

| Ticker | Score | RSI | MACD vs signal | Trend | Scan reward_risk |
|---|---|---|---|---|---|
| AMGN | 92.5 | 54.86 | 1.26 > 0.45 | up | 1.46 (drop) |
| GILD | 78.0 | 59.42 | 0.74 < 1.2 | up | 1.66 (drop) |
| REGN | 64.7 | 42.13 | -14.26 < -10.91 | up (price below 50d 789.47) | 1.22 (drop) |
| VRTX | 59.7 | 45.61 | -4.58 < -3.23 | up (price below 50d 520.46, above 200d 474.9) | 2.09 |
| ISRG | 55.8 | 66.74 | 9.45 > 7.83 | DOWN (drop) | 1.31 |

**Pick: VRTX** (only name passing both filters).

Scan suggested_levels (reward_risk 2.09):
- entry_low 503.72 (0.382 retracement), entry_high 510.08 (current price)
- target 560.25 (swing high)
- stop 481.4
- reward_risk 2.09 (as computed by the scan, consistent with a mid-zone entry of about 506.9)
No adjustments made to the levels. Note that from entry_high alone the ratio is about 1.75 (50.17 up / 28.68 down); from entry_low about 2.53. Only buying in the lower part of the zone gives well above 2.0.

Runner-up: GILD (score 78.0, RSI 59.42, price 151.17, 50d 144.22). It fails min_reward_risk at 1.66 (entry 146.11-151.17, target 163.52, stop 139.69), so it is a watch only. AMGN has the top score but is 1.46.

Reasoning: VRTX is the only Health Care name with an up Fibonacci trend and reward_risk of at least 2.0. Price sits right at the 0.382 retracement (503.72), a common pullback stop, which gives a close stop at 481.4. Caveats: momentum is weak (RSI 45.61, MACD below signal, price under the 50-day average), and its score is low (59.7), so the setup relies on the support holding. Prefer entries toward 503.72.
