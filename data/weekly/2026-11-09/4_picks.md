# Final picks, week of 2026-11-09

No picks this week in either sector. Alerts would watch Monday 2026-11-09 through Friday 2026-11-13 (valid_until). With no picks, only data/watchlist.json stocks (if any) are checked. Rules applied as written in config/strategy.json (version 2): reward to risk of at least 2.0 on the scan's own suggested_levels (target minus middle of buy zone, divided by middle of buy zone minus stop), stop no more than 10% below the top of the buy zone, and chart and news checks. All prices come from data/technical_scan.json (created 2026-11-03, 11:00 PM New York, after the close). Research, not financial advice.

## Picks

| Sector | Ticker | Buy zone | Target | Stop | R/R (scan) | Source |
|---|---|---|---|---|---|---|
| Health Care | none | - | - | - | - | - |
| Consumer Staples | none | - | - | - | - | - |

## Why no pick

### Health Care

| Ticker | Picked by | Buy zone | Target | Stop | R/R (scan) | Result |
|---|---|---|---|---|---|---|
| ALNY | qualitative | 153.87 - 158.62 | 208.86 | 144.71 | 4.56 | Fails chart check: downtrend, technical score 0.0 |
| GILD | technical (closest) | 162.50 - 170.79 | 190.81 | 152.82 | 1.75 | Fails 2.0, RSI 73.96 |
| AMGN | technical runner-up | 438.71 - 465.36 | 518.23 | 411.69 | 1.64 | Fails 2.0, reported Nov 3 |
| GEHC | qualitative runner-up | 75.52 - 79.65 | 85.90 | 71.81 | 1.44 | Fails 2.0 |

The agents disagreed (no technical pick vs ALNY). ALNY has strong sales growth and the biggest analyst upside, but the chart is the problem. It is in a downtrend from a swing high of 380.00 and sits right on its swing low of 156.00. Its "target" of 208.86 is only the first bounce level in a falling stock, and its high R/R of 4.56 just means the stop is close. The picker rules say a qualitative pick needs a chart that is not in a downtrend, so it fails. Its 633.5% earnings growth is also mostly a one-time tax gain. GILD has the best chart but fails 2.0, and its RSI of 73.96 is close to the 75 limit.

### Consumer Staples

| Ticker | Picked by | Buy zone | Target | Stop | R/R | Result |
|---|---|---|---|---|---|---|
| MDLZ | both (scan stop) | 64.31 - 65.41 | 69.00 | 62.34 | 1.64 (scan) | Fails 2.0 |
| MDLZ | technical (moved stop) | 64.31 - 65.41 | 69.00 | 62.97 | 2.19 (agent's own math) | Not accepted, see below |
| KDP | runner-up for both | 33.32 - 34.65 | 36.95 | 31.88 | 1.41 (scan) | Fails 2.0, reported Nov 3 |

Both agents chose MDLZ, which is normally a strong signal. The chart is clean (uptrend, RSI 60.99) and earnings just beat with the outlook confirmed. The problem is the levels. On the scan's own levels, reward to risk is 1.64, below 2.0.

The technical agent moved the stop up to the 0.382 Fibonacci line (62.97) to get 2.19. The price is in the scan file, so it is not made up. But I did not accept it, for three reasons:
- It was chosen to pass the rule, not because it is a better place for a stop. The scan puts its stop (62.34) below the 0.382 line on purpose. A stop right on a support line gets hit by a normal test of that line.
- The agent itself called it a marginal pass, with the stop only about 1.34 below the bottom of the buy zone.
- Last week the picker refused hand-adjusted targets for the same reason. Changing how levels are set is a strategy change, and that needs Top's approval.

## What would make me wrong

- MDLZ could keep grinding up toward 69.00 without a deep dip. Then a steady, low-risk trade was missed. If you want it anyway, that is an exception for you to approve (as with NVDA on 2026-10-05). In that case use a smaller position, and know that a dip to 62.97 would stop you out.
- ALNY could bounce hard from its swing low, since sales are growing fast and analysts see big upside. Buying a falling stock at its low is a guess on the turn, not a setup these rules allow.
- GILD could pull back toward the 0.236 level (162.50) or the 0.382 level (154.36). A new scan would then give better levels. No level here should be adjusted by hand.

## Watch, not buy

- MDLZ: a pullback into the low end of the zone, or a new scan with levels that pass 2.0.
- GILD: a cooler RSI and a pullback toward 154.36 to 162.50, confirmed by a new scan.
- KDP and AMGN: both reported Nov 3. Look at them again only after the price reaction is clear.

This is the fourth week in five with no rule-based pick in at least one sector, and the second in a row with none in either. The 2026-11-03 review said to bring this to Top if the rule-based pick rate stays near 1 in 6 sector slots for 3 or more weeks. The review suggested looking at how scripts/indicators.py sets targets, not at the 2.0 floor. It is worth raising at the next /weekly-review. A missed trade costs nothing.
