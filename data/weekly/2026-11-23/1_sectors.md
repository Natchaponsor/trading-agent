# Sector Rotation - week of 2026-11-23

Source data: `data/sector_scan.json` (created 2026-11-22T13:52-05:00, Sunday, so it uses Friday 2026-11-20 closing prices). The Wikipedia stock list refresh failed this run, so the saved Nasdaq-100 list in `config/universe_nasdaq100.csv` was used. Research, not financial advice.

## Big picture

The US market is falling hard. The Nasdaq-100 (QQQ) is down 13.63% over 1 month and 13.77% over 3 months, and the S&P 500 (SPY) is down 9.71% over 1 month. All are below their 200-day averages, including small caps (IWM, down 7.25% in a month). World markets are falling with the US, not against it: developed markets (EFA) are down 6.8% and emerging markets (EEM) are down 12.77% over 1 month, both below their 200-day averages. The 10-year yield (^TNX) is 4.91, slightly lower this month (down 0.83%) but up 4.42% over 3 months and above its 200-day average, so rates are still high. Fear is very high: VIX is 35.89, far above 20, and up 88.6% in a month.

News context: CNBC says the S&P 500 fell about 8.6% and the Nasdaq about 10% last week, led by an AI and chip selloff (Nvidia fell about 14% on Friday), and the S&P 500 and Dow closed in correction.

## Ranked sectors (top 5, all eligible)

Positive numbers mean the sector beat QQQ by that many percentage points.

| Rank | Sector | ETF | Score | ETF vs QQQ 1m / 3m / 6m | Members median vs QQQ 1m / 3m / 6m | ETF above 50-day | Members |
|---|---|---|---|---|---|---|---|
| 1 | Health Care | XLV | 20.4 | 11.39 / 15.61 / 34.24 | 14.91 / 20.59 / 35.91 | Yes | 9 |
| 2 | Consumer Staples | XLP | 17.48 | 14.15 / 17.89 / 23.14 | 14.84 / 15.69 / 24.81 | Yes | 6 |
| 3 | Utilities | XLU | 13.96 | 13.21 / 13.27 / 10.45 | 12.14 / 17.14 / 12.97 | Yes | 4 |
| 4 | Consumer Discretionary | XLY | 9.25 | 11.41 / 9.04 / 9.78 | 12.21 / 7.24 / 7.7 | No | 17 |
| 5 | Industrials | XLI | 8.19 | 7.42 / 1.36 / 6.53 | 9.39 / 6.64 / 23.51 | No | 11 |

Not eligible (too few Nasdaq-100 members): Basic Materials (score 11.43), Financials (11.07), Real Estate (10.55), Energy (1.11). Technology is #7 with a score of -6.11, and its ETF is below its 50-day average.

Note: most of the gap comes from QQQ falling, not from these sectors rising a lot. These are "lose less" leaders in a tech selloff. Only the top 3 have their ETF above the 50-day average.

## Choices

**1. Health Care (XLV).** Top score (20.4) and #1 again, so the lead is lasting. It beats QQQ over every time frame, and the typical Nasdaq-100 member beat it by 35.91 points over 6 months. CNBC reports Johnson & Johnson rose about 1% on Friday as investors moved into defensive stocks, while tech dropped more than 5%. Yahoo Finance notes health care is still positive for the year.

**2. Consumer Staples (XLP).** Score 17.48, up from 12.58 in the 2026-11-09 report. The ETF beat QQQ by 14.15 points over 1 month and 17.89 over 3 months, and its 6-month gap (23.14) is now strong too. Yahoo Finance says staples was the standout sector on Friday, up 1.7%, and CNBC says Procter & Gamble and Costco gained. Weak spot: only 6 Nasdaq-100 members, so the stock list is short.

**Swap decision:** No swap. Utilities (#3, score 13.96) is close, and its ETF is above its 50-day average. But it trails both picks over 6 months (ETF 10.45, members 12.97) and has only 4 members. Utilities are also the most rate-sensitive group, and CNBC says markets strongly expect a quarter-point Fed hike on Dec 8-9. I found no news that clearly favors Utilities over Staples.

## Risks to watch

- **Sharp tech bounce.** After a roughly 10% weekly drop in the Nasdaq (CNBC), a fast rebound is possible. If chips bounce, defensive sectors will likely trail QQQ for a while, even if they stay positive.
- **Crowded and pricey defensives.** Trustnet reports BofA's bubble-risk gauge flags US health care as showing "extreme bubble-like dynamics," with staples not far behind. Crowded trades can reverse quickly when fear fades.
- **PCE inflation and Q3 GDP, Wed Nov 25.** Per FX Empire and Tradingkey, consensus is headline PCE 3.8% (from 3.6%) and core 3.2% (from 3.1%). A hot number would firm up the December hike, which can weigh on rate-sensitive staples.
- **Holiday-thin trading.** Markets are closed Thu Nov 26 and close early Fri Nov 27. Thin trading with VIX at 35.89 can mean big swings.
- **Earnings this week.** Dell (Tue Nov 24) and HPE are AI hardware bellwethers. Strong results could lift tech. Agilent (health care tools) reports Monday, and Dollar Tree (a discount retailer that competes with staples names) reports this week. Black Friday gives a first read on holiday spending.
- **Nvidia and AI news.** CNBC cites a Reuters report that the SEC is exploring possible accounting issues at Nvidia. More bad AI news would likely extend the defensive lead; good news could end it.
- **Weak world markets.** EEM is down 12.77% in a month and EFA down 6.8%, both below their 200-day averages.

## News used

- [Stock market news for Nov. 20, 2026 (CNBC)](https://www.cnbc.com/2026/11/19/stock-market-today-live-updates.html)
- [Markets News, Nov. 20, 2026: Major Stock Indexes Sink, Wipe Out 2026 Gains as AI Trade Melts Down (Yahoo Finance)](https://finance.yahoo.com/markets/stocks/articles/stock-market-today-futures-plunge-131303598.html)
- [This Is a Huge Week for the Stock Market: Nvidia Earnings, Fed Minutes, and Anthropic's IPO (Mitrade/Motley Fool, 2026-11-17)](https://www.mitrade.com/insights/news/live-news/article-8-2258057-20261117)
- [The Week Ahead: PCE in Focus After AI Sell-Off in Holiday-Shortened Week (FX Empire)](https://www.fxempire.com/forecasts/article/the-week-ahead-pce-in-focus-after-ai-sell-off-in-holiday-shortened-week-1646337)
- [The Week Ahead: US Q3 GDP and October PCE Due on Same Day, Dell and HPE Report Earnings (Tradingkey)](https://www.tradingkey.com/analysis/stocks/us-stocks/262316778-week-ahead-us-gdp-pce-dell-hpe-report-anthropic-tradingkey)
- [Tech rotation creating bubble-like dynamics in defensive stocks (Trustnet)](https://www.trustnet.com/news/13488327/tech-rotation-creating-bubble-like-dynamics-in-defensive-stocks)
- [Consumer Staples Post Their Best Month Since 1998 as Investors Retreat From AI Stocks (European Business Magazine)](https://europeanbusinessmagazine.com/consumer-staples-post-best-month/)
