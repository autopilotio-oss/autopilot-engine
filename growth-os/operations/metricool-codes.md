# Metricool field codes (looked up 2026-11-04, so runs skip getAnalyticsAvailableMetrics)
- Threads posts: THPO02 time, THPO03 text, THPO07 type, THPO08 views, THPO09 likes, THPO10 replies, THPO11 reposts, THPO12 quotes, THPO13 shares. Evolution: THEV06 views, THEV05 interactions, THEV01 followers.
- TikTok posts: TKPO02 time, TKPO05 text, TKPO07 views, TKPO08 likes, TKPO09 comments, TKPO10 shares, TKPO13 full watch rate, TKPO22 type. Evolution TKEV02 = daily views (matches post sums).
- Instagram feed posts: IGPO02 time, IGPO03 text, IGPO07 type, IGPO28 views, IGPO14 reach, IGPO15 saved, IGPO27 shares, IGPO08 comments, IGPO29 follows.
- X: no "posts" connector; valid connectors are evolution and tw. TTTW* returned text only, metrics null.
- Ask one network per call: mixed network post calls return only one network.
