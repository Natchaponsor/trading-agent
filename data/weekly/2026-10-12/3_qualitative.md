# Qualitative Review - week of 2026-10-12

Sources: `data/qualitative_data.json` (created 2026-10-12T02:05-04:00), `data/technical_scan.json` (prices through Fri 2026-10-09), `config/strategy.json`. Research, not financial advice.

**Data-quality warning on news.** The web search tool returned mostly undated or stale pages, and several searches were rate-limited (AVGO first try, NBIS, DXCM, IDXX, AMGN). Many "October 2026" snippets mixed in 2025 events or conflicting dates (for example, WDC earnings shown as Oct 29 in search vs Oct 22 in the data file; the STX "Oct 29 +19%" item looks like a 2025 event). I use the data-file dates. Ratings below are therefore low confidence, and "neutral (unverified)" means I found no verifiable negative or positive item from the last 2 weeks. Verify headlines before trading.

## Technology

Eleven stocks tie at numbers_score 100.0. I reviewed all eleven, not the first five in file order: APP, AVGO, CRWV, MCHP, MU, MPWR, NBIS, NVDA, SNDK, STX, WDC. I ranked them on growth quality (profitable, positive earnings growth, sane forward P/E), news, and reward to risk from technical_scan.

| Ticker | Rev growth | Earn growth | Fwd P/E | Analyst upside | Next earnings | News | Growth quality note |
|---|---|---|---|---|---|---|---|
| MU | 379.3% | 1060.1% | 4.99 | 51.13% | 2026-12-23 | Neutral | Profit margin 63.8%, 46 analysts, earnings far away |
| NVDA | 105.9% | 127.8% | 14.41 | 43.37% | 2026-11-17 | Neutral to positive | Margin 63.7%, 59 analysts, largest company |
| WDC | 43.8% | 984.1% | 12.40 | 69.53% | 2026-10-22 | Neutral (unverified) | Margin 72.9%, but earnings in 11 days and RR 0.84 |
| STX | 48.5% | 148.8% | 13.88 | 46.15% | 2026-10-27 | Neutral (unverified) | Margin 26.1%, RR 0.42 |
| MPWR | 47.6% | 85.8% | 39.64 | 32.71% | 2026-10-29 | Positive | Margin 24.5%, rich P/E, only 15 analysts |
| SNDK | 371.6% | n/a | 5.94 | 37.37% | 2026-10-29 | Neutral | Margin 56.5%, RR 0.83 |
| AVGO | 85.5% | 215.3% | 18.64 | 46.96% | 2026-12-09 | Neutral (unverified) | Margin 42.9%, RR 0.68 |
| APP | 52.8% | 57.0% | 13.33 | 78.94% | 2026-11-04 | Negative | Margin 64.6%, but regulatory/short-seller headlines and deep drawdown |
| CRWV | 112.5% | n/a | -45.28 | 72.36% | 2026-11-11 | Neutral | Margin -25.4%, loss-making, heavy capital raising |
| NBIS | 454.0% | n/a | -62.13 | 28.29% | 2026-11-10 | Neutral to positive | Margin 3.1%, loss-making forward P/E |
| MCHP | 38.0% | n/a | 16.48 | 42.74% | 2026-11-05 | Neutral | Margin 9.3%, trailing P/E 111 |

None has earnings_within_avoid_window true. WDC (Oct 22) and STX (Oct 27) report soonest; both have poor RR anyway.

### Pick: Micron (MU)

- Current price 1029.00. Fibonacci trend up (swing 408.44 to 1254.81).
- Levels used: technical_scan suggested_levels unchanged. entry_low 931.49 (0.382 retracement), entry_high 1029.00, target 1254.81 (prior swing high), stop 823.31.
- Analyst mean target 1555.13 is higher than 1254.81, so the analyst override does not apply.
- Reward to risk: 1.75 per the scan (measured from the zone midpoint 980.25). Buying at the top of the zone gives 1.10 ((1254.81-1029.00)/(1029.00-823.31)). Better to scale in toward the lower half of the zone.
- Reasoning: MU has the highest growth in the tied group (revenue +379.3%, earnings +1060.1%) with a 63.8% margin and a forward P/E of 4.99, so the growth is real profit, not a loss-making build-out. Its earnings date (2026-12-23) is the furthest away of all candidates, so no event risk this month. The news is mixed: the stock is well off its late-June high, with worry over raised capex and Alphabet's TurboQuant memory-reduction tech, but Mizuho kept Outperform with a $1,375 target and memory supply is described as tight into 2027. Risk: a memory-cycle turn; price is 18% below the swing high, so the stop at 823.31 is about 20% below.

### Runner-up: Nvidia (NVDA)

- Price 229.28, trend up. Levels: entry_low 221.19, entry_high 229.28, target 243.37, stop 212.20 (suggested_levels; analyst mean 328.72 is higher, so no override). RR 1.39 per scan.
- Revenue +105.9%, earnings +127.8%, forward P/E 14.41, 59 analysts. News is neutral to positive; a risk is a chip-export-restriction headline (search showed this theme, dates unverified). Earnings 2026-11-17.

### Why not the others

APP has the best scan RR (3.86) but news is negative (SEC/short-seller items, dates unverified), the stock is in a downtrend near its swing low, and the target of 350.66 is a counter-trend bounce. AVGO, STX, WDC, SNDK, NBIS, CRWV have scan RR below 1. MPWR is RR 1.05 with a 39.6 forward P/E. MCHP has weak margin and RR 1.27.

### News links (Technology)

- NVDA, neutral to positive: https://www.tipranks.com/stocks/nvda/stock-news (aggregated news; 90% positive coverage claim, undated)
- MU, neutral: https://www.barchart.com/story/news/1090050/should-you-buy-micron-stock-after-its-32-decline (capex and TurboQuant overhang); https://www.nasdaq.com/articles/micron-gains-momentum-again-30-80-upside-2026
- MPWR, positive: https://seekingalpha.com/news/4512027-monolithic-power-systems-signals-enterprise-data-segment-growth-of-30-40-percent-in-2026 (data-center growth outlook); earnings Oct 29 per https://unusualwhales.com/stock/MPWR/earnings
- WDC, neutral (unverified): https://unusualwhales.com/stock/WDC/earnings
- STX, neutral (unverified): https://finance.yahoo.com/news/seagate-technology-stock-wall-street-170340863.html
- SNDK, neutral: https://finance.yahoo.com/markets/stocks/articles/sandisk-sndk-surges-550-2026-175957395.html
- AVGO, neutral (unverified, old items): https://www.tradingview.com/symbols/Nasdaq-AVGO
- APP, negative: https://www.marketbeat.com/instant-alerts/price-applovin-nasdaq-app-trading-down-63-heres-why-2026-09-23/ ; https://www.nasdaq.com/articles/why-applovin-stock-was-falling-today
- CRWV, neutral: https://finance.yahoo.com/markets/stocks/articles/coreweave-raised-20-billion-capital-144406639.html (JPM upgrade Sept 24, $20B raised this year)
- NBIS, neutral to positive: https://www.marketbeat.com/instant-alerts/nebius-group-nasdaqnbis-trading-up-13-heres-what-happened-2026-07-23/ (older than 2 weeks)
- MCHP, neutral: https://www.nasdaq.com/articles/can-microchips-expanding-portfolio-help-its-stock-deliver-2026

## Health Care

Only 9 stocks were checked; top 5 by numbers_score.

| Ticker | Rev growth | Earn growth | Fwd P/E | Analyst upside | Next earnings | News |
|---|---|---|---|---|---|---|
| ALNY | 66.9% | n/a | 18.73 | 59.42% | 2026-10-29 | Negative |
| DXCM | 13.1% | 43.6% | 26.90 | 14.41% | 2026-10-29 | Neutral (unverified) |
| ISRG | 18.5% | 26.5% | 35.02 | 12.62% | 2026-10-20 | Neutral |
| IDXX | 9.7% | 17.6% | 30.95 | 35.39% | 2026-11-02 | Neutral (unverified, search failed) |
| AMGN | 9.5% | 64.9% | 16.94 | -5.39% | 2026-11-03 | Neutral (unverified, search failed) |

No stock is flagged earnings_within_avoid_window. ISRG reports Oct 20 (9 days out) and DXCM and ALNY Oct 29.

### Pick: DexCom (DXCM)

- Current price 84.11, trend up (swing 56.72 to 92.59).
- Levels used: suggested_levels unchanged. entry_low 78.89 (0.382 retracement), entry_high 84.11, target 92.59 (swing high), stop 73.91. Analyst mean target 96.23 is higher than 92.59, so no override.
- Reward to risk: 1.46 per the scan (zone midpoint 81.50). At the top of the zone it is 0.83, so only buy toward the lower half (about 78.89 to 81.50).
- Reasoning: DXCM has the best mix of growth and technical setup in this sector: revenue +13.1%, earnings +43.6%, a 20.1% margin, and a technical score of 54.7 in an uptrend. ALNY has stronger revenue growth but negative news (2026 guidance cut and a large post-earnings drop in the search snippets) and a scan RR of 0.35. AMGN's price (414.87) is above the analyst mean (392.50) so it has no analyst upside. Weak spots: the sector is the second-ranked sector with a negative score, DXCM earnings fall Oct 29 (not in the 5-day avoid window until Oct 24), and I could not verify any DXCM news from the last 2 weeks (search was rate-limited; the search returned old G7 and short-seller Hunterbrook items). Treat the news rating as unverified and check headlines before entry. Plan to exit or reduce before Oct 29 if the setup is not working.

### Runner-up: Intuitive Surgical (ISRG)

- Price 423.96, trend down. Levels: entry_low 409.86, entry_high 423.96, target 456.36, stop 386.77 (suggested_levels; analyst mean 477.47 is higher, no override). RR 1.31 per scan.
- Revenue +18.5%, earnings +26.5%, forward P/E 35.02. News neutral: stock down 10.31% since last earnings on tight hospital capex and rival robots, though 100% of analysts rate it a buy. Earnings Oct 20, so event risk is near.

### News links (Health Care)

- ALNY, negative: https://www.opencapital.sh/stocks/alny/earnings/q2-2026 (2026 revenue guidance lowered); https://unusualwhales.com/stock/ALNY/earnings
- DXCM, neutral (unverified, older): https://www.zacks.com/stock/news/2447961/dexcom-shares-may-rise-as-g7-15-day-cgm-system-gets-fda-clearance
- ISRG, neutral: https://unusualwhales.com/stock/ISRG/earnings ; https://www.simplywall.st/stocks/us/healthcare/nasdaq-isrg/intuitive-surgical/future
- IDXX, AMGN: no usable news retrieved (search rate-limited).

## Summary

| Sector | Pick | Entry zone | Target | Stop | RR (scan, midpoint) | RR at entry_high | Runner-up |
|---|---|---|---|---|---|---|---|
| Technology | MU | 931.49 to 1029.00 | 1254.81 | 823.31 | 1.75 | 1.10 | NVDA |
| Health Care | DXCM | 78.89 to 84.11 | 92.59 | 73.91 | 1.46 | 0.83 | ISRG |
