---
description: Review past picks with the feedback agent and decide on strategy changes
---
1. Use the feedback agent to review past performance.
2. Show me the scoreboard and each proposed change (setting, old value, new value, evidence).
3. For each proposed change, ask me to approve or reject it.
4. For each approved change only: edit config/strategy.json, raise "version" by 1, set "last_changed" to today, and add an entry to "change_log" with date, version, change, reason and "approved_by": "Top".
5. Do not change anything I did not approve.
