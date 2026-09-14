# SupplyNow Atlas

Indexed search, relationship map, plain-language Q&A and a request log built from the
Contract Facts Ledger (Version 14, Sep 14, 2026).

Published artifact: https://claude.ai/artifact/RZ2yG4TZjNqif4kGPeLKya

- `atlas.html` — the page (styles, markup, search engine, d3 map, chat, request log, activity scores).
- `kb.js` — the knowledge base: entities, facts (definition / moment / decision / number / open / finding), relationships.

The page declares two runtime capabilities when published as an artifact: `db` (shared request log
and per-user activity) and `sample` (ask the ledger). Without them it still searches and maps.

To update the index: edit `kb.js`, republish `atlas.html` with `kb.js` as a supporting file.
