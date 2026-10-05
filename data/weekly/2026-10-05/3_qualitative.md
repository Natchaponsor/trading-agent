# Qualitative Review - week of 2026-10-05

Sources: `data/qualitative_data.json` (created 2026-10-04T16:41-04:00), `data/technical_scan.json` (same timestamp), linked web pages. Research, not financial advice.

Method notes
- Top 5 by numbers_score. In Technology, 10 stocks tie at 100.0; I took the first five in the file's ranked order (APP, AVGO, CRWV, MCHP, MU). Other 100.0 names not reviewed: MPWR, NVDA, STX, WDC (and SNDK at 98.8).
- Growth figures are year over year. "n/a" means the field is null in the data.
- News caveat: the search tool mostly returned older articles. A "neutral" rating below often means I found no dated news from the last 2 weeks, not that I confirmed a quiet period. Only APP and ALNY had clear recent negative evidence; I flag the dating where it is unclear.
- Reward to risk (R/R) is computed from the midpoint of the entry zone, matching the scan's `reward_risk`. All of this week's candidates are below the config minimum of 2.0 except APP (negative news).

## Technology

| Ticker | Rev growth | Earnings growth | Fwd P/E | Analyst upside | Next earnings | News |
|---|---|---|---|---|---|---|
| APP | 52.8% | 57.0% | 12.8 | 85.3% | 2026-11-04 | Negative |
| AVGO | 85.5% | 215.3% | 18.3 | 49.6% | 2026-12-09 | Neutral |
| CRWV | 112.5% | n/a | -49.6 (loss-making) | 58.0% | 2026-11-11 | Neutral |
| MCHP | 38.0% | n/a | 17.7 | 32.6% | 2026-11-05 | Neutral |
| MU | 379.3% | 1060.5% | 5.2 | 41.4% | 2026-12-23 | Positive |

News evidence
- APP, negative: securities class action filed in mid-September over its AI claims, BofA and Piper Sandler cut to Neutral after the Q2 revenue miss, stock down 54% in 2026. [TIKR](https://www.tikr.com/blog/applovin-stock-is-down-54-in-2026-and-facing-a-class-action-heres-where-it-could-go), [ad-hoc-news](https://www.ad-hoc-news.de/boerse/news/corporate-news/applovin-corp-stock-falls-to-usd-324-74-as-targets-diverge/70158826)
- AVGO, neutral: only older items found (VMware extension, partnerships), nothing dated in the last 2 weeks. [TradersUnion](https://tradersunion.com/news/financial-news/show/2172324-broadcom-advances-3-39percent-this-week/)
- CRWV, neutral: no dated recent news found; background is a large backlog but heavy customer concentration. [Yahoo Finance](https://finance.yahoo.com/news/coreweave-seeks-8-5b-funding-162206262.html)
- MCHP, neutral: no dated recent news found; consensus Strong Buy, last results in line on revenue. [Barchart](https://www.barchart.com/story/news/559273/microchip-technology-stock-is-mchp-outperforming-the-technology-sector)
- MU, positive: fiscal Q4 guidance of about $50B revenue and EPS near $31, 2026 HBM output sold out under fixed-price contracts. The Sept 30 earnings result itself was not confirmed in my search, so verify it before entry. [Sentisense](https://app.sentisense.ai/stories/micron-targets-doubling-hbm-capacity-amid-fed-rate-risk-and-strong-q4-outlook-09042026), [Kapitalmarktexperten](https://www.kapitalmarktexperten.de/micron-technology-aktie-hbm-produktion-2026-ausverkauft/)

### Pick: Micron (MU)
Levels come from `suggested_levels` in technical_scan.json. The analyst mean target is 1520.02, above the suggested target, so the suggested target is kept.

| Entry low | Entry high | Target | Stop | R/R (midpoint) |
|---|---|---|---|---|
| 1044.59 | 1074.89 | 1254.81 | 905.39 | 1.26 |

Current price 1074.89. Target is the swing high (1254.81); stop is below the 0.382 retracement (914.54).

Reasoning: MU has the strongest growth in the group (revenue +379%, earnings +1060%) at a forward P/E of 5.2, and its news is positive on sold-out HBM and strong guidance. Next earnings is 2026-12-23, so there is no earnings risk inside the 5-day window. Warnings: R/R of 1.26 is below the 2.0 minimum, and the stop is 15.8% below the current price, above the 10% max_stop_distance_pct in config. Price is also near its swing high (1254.81 vs 1074.89), so this is a momentum name that has already run.

### Runner-up: Broadcom (AVGO)
Revenue +85.5%, earnings +215%, neutral news, no earnings in the window. Suggested levels: entry 348.62 to 355.14, target 379.55, stop 306.13, R/R 0.60 (analyst target 531.31 is higher, so suggested target kept). The R/R is poor, which is why it is second.

Not chosen: APP has the best suggested R/R (4.43, entry 260.17 to 268.22, target 350.66, stop 244.69) but a fresh class action and downgrades make it a negative-news name, and its price sits near the 266.84 swing low in a downtrend.

## Health Care

| Ticker | Rev growth | Earnings growth | Fwd P/E | Analyst upside | Next earnings | News |
|---|---|---|---|---|---|---|
| ALNY | 66.9% | n/a | 17.6 | 68.9% | 2026-10-29 | Negative |
| ISRG | 18.5% | 26.5% | 32.4 | 21.5% | 2026-10-20 | Neutral |
| DXCM | 13.1% | 43.6% | 27.3 | 11.4% | 2026-10-29 | Positive |
| IDXX | 9.7% | 17.6% | 31.0 | 35.3% | 2026-11-02 | Neutral |
| AMGN | 9.5% | 64.9% | 16.5 | -3.0% | 2026-11-03 | Positive |

News evidence
- ALNY, negative: stock fell about 28% after Q2 as Alnylam cut its 2026 ATTR revenue guidance by $200M at both ends and Amvuttra sales missed by 4%. That was in August, so it is not strictly within 2 weeks, but it is the live overhang. [Fierce Pharma](https://www.fiercepharma.com/pharma/alnylam-shares-tank-27-amvuttra-disappoints-attr-outlook-cut-2026)
- ISRG, neutral: Q1 2026 was a strong beat (revenue +23%), nothing newer found. [TipRanks](https://www.tipranks.com/news/intuitive-surgical-stock-nasdaqisrg-gains-after-q1-earnings-beat)
- DXCM, positive: Q2 revenue +13.1% to $1.31B and full-year guidance raised to $5.18B-$5.25B, stock jumped 16.6%. Exact report date was not shown in the snippet, so it is probably August, not the last 2 weeks. [iTiger](https://www.itiger.com/hans/news/2493752475)
- IDXX, neutral: no dated recent news found; stock is well off its 52-week high. [Yahoo Finance](https://finance.yahoo.com/news/idexx-laboratories-stock-performance-compared-072924601.html)
- AMGN, positive: Q2 2026 beat (revenue +9.5% to $10.05B, EPS beat by 12%) and raised full-year guidance. Date is August, not the last 2 weeks. [StockStory](https://stocks.observer-reporter.com/observerreporter/article/stockstory-2026-7-2-amgen-amgn-stock-is-up-what-you-need-to-know)

### Pick: DexCom (DXCM)
Levels come from `suggested_levels`. The analyst mean target is 95.08, above the suggested 92.59, so the suggested target is kept.

| Entry low | Entry high | Target | Stop | R/R (midpoint) |
|---|---|---|---|---|
| 84.12 | 85.36 | 92.59 | 78.10 | 1.18 |

Current price 85.36. Entry is at the 0.236 retracement (84.12); target is the swing high (92.59).

Reasoning: DXCM combines double-digit revenue growth (+13.1%), 43.6% earnings growth and a guidance raise, with an uptrend in the technical scan. It is the only reviewed name with growth, positive news and a usable setup together, since ALNY has stronger growth but a guidance cut, and AMGN has negative analyst upside (-3.0%). Earnings are 2026-10-29, 25 days out, so outside the 5-day avoid window. Warnings: R/R of 1.18 is below the 2.0 minimum, analyst upside is only 11.4%, and Health Care itself is lagging QQQ and below its 50-day average (see 1_sectors.md). Stop distance is 8.5%, inside the 10% cap.

### Runner-up: Intuitive Surgical (ISRG)
Revenue +18.5%, earnings +26.5%, neutral news, earnings 2026-10-20 (16 days out, outside the window). Suggested levels: entry 390.68 to 391.95, target 409.86, stop 363.27, R/R 0.66 (analyst target 476.34 is higher, so suggested target kept). Weak R/R, and it is in a downtrend.
