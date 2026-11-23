# Final picks, week of 2026-11-23

No picks this week in either sector. Alerts would watch Monday 2026-11-23 through Friday 2026-11-27 (valid_until). Markets are closed Thursday 2026-11-26 for Thanksgiving. With no picks, only data/watchlist.json stocks (if any) are checked.

Rules applied as written in config/strategy.json (version 2): reward to risk of at least 2.0 (technical.min_reward_risk) on the scan's own suggested_levels, stop no more than 10% below the top of the buy zone, and the chart and news checks. All prices and ratios come from data/technical_scan.json (created 2026-11-22 14:00 New York) and data/qualitative_data.json. Research, not financial advice.

## Picks

| Sector | Ticker | Buy zone | Target | Stop | R/R (scan) | Source |
|---|---|---|---|---|---|---|
| Health Care | none | - | - | - | - | - |
| Consumer Staples | none | - | - | - | - | - |

## Why no pick

### Health Care

| Ticker | Picked by | Buy zone | Target | Stop | R/R (scan) | Result |
|---|---|---|---|---|---|---|
| IDXX | technical | 663.44 - 676.21 | 713.74 | 626.00 | 1.00 | Fails 2.0 |
| GEHC | technical runner-up | 76.99 - 80.64 | 87.56 | 72.99 | 1.50 | Fails 2.0 |
| ALNY | qualitative | 139.51 - 143.82 | 199.24 | 131.20 | 5.51 | Fails chart check: downtrend, technical score 12.0 |
| REGN | qualitative runner-up | 896.20 - 920.69 | 990.72 | 829.36 | 1.04 | Fails 2.0 |

The agents disagreed (IDXX vs ALNY). IDXX has the best chart, but the scan's target is its swing high of 713.74, which gives a reward to risk of only 1.00. The technical report moved the target up to the 1.272 extension (771.71) to get about 2.32. I did not use that. It is not script output, and that target method is not in the approved strategy. Changing how targets are set needs Top's approval.

ALNY passes 2.0 on the scan's own levels, but the picker rules say a qualitative pick needs a chart that is not in a downtrend. ALNY is falling from a swing high of 380.00 and sits on its swing low of 143.40. Its high ratio mostly reflects a close stop under a falling stock. It failed for the same reason in week 2026-11-09.

No other Health Care stock in the scan reaches 2.0 (best is AMGN at 1.71, which also has a weak RSI of 42.41).

### Consumer Staples

| Ticker | Picked by | Buy zone | Target | Stop | R/R (scan) | Result |
|---|---|---|---|---|---|---|
| KHC | technical | 25.34 - 25.39 | 26.22 | 24.39 | 0.87 | Fails 2.0 |
| MDLZ | technical runner-up and qualitative runner-up | 66.17 - 66.28 | 68.92 | 63.83 | 1.12 | Fails 2.0 |
| KDP | qualitative | 34.53 - 34.84 | 35.97 | 33.04 | 0.78 | Fails 2.0 |
| CCEP | (best ratio in sector) | 111.51 - 115.53 | 127.13 | 105.95 | 1.80 | Fails 2.0, negative analyst upside |

KHC has the strongest chart in the group, with the only rising MACD. But the scan's target (26.22) is barely above the buy zone, so reward to risk is 0.87. The technical report's 1.272 extension target (29.29, about 4.03) was not used, for the same reason as IDXX. That target would also need KHC to break well above its swing high of 27.65. KDP's own report called it low conviction, and its ratio is 0.78. No stock in the sector reaches 2.0.

## What would make me wrong

- IDXX could keep its uptrend and break above 713.74. Then a strong stock was skipped because the target rule only looks as far as the last high. That is a question for the rules, not for this week's pick.
- KHC could follow through on its rising MACD and push to new highs. Same reason.
- ALNY could bounce hard from its low, since analysts see big upside and the news is good. Buying a falling stock at its low is a guess on the turn, not a setup these rules allow.
- The wider market is weak (QQQ down 13.63% over 1 month, VIX 35.89 per data/sector_scan.json). In a market like this, sitting out is a reasonable result. A missed trade costs nothing.

## Watch, not buy

- IDXX and GEHC: a pullback toward lower support, followed by a new scan with levels that pass 2.0.
- KHC: a new scan after any move above 26.22, which would change its levels.
- ALNY: only after the chart stops making new lows and the scan calls the trend up.

## For the next review

This is the third run in a row with no picks. The 2026-11-22 review said the pick-rate trigger has been met and suggested looking at the target rule in scripts/indicators.py with Top. This week shows the issue clearly: IDXX and KHC fail only because their targets are capped at the last swing high or a nearby retracement. Any change, such as using extension targets, needs Top's approval, a test, and a strategy version bump before the picker can use it.
