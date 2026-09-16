# SupplyNow Atlas

Indexed search, relationship map, plain-language Q&A and a request log built from the
Contract Facts Ledger (Version 14, Sep 14, 2026).

Published artifact: https://claude.ai/artifact/RZ2yG4TZjNqif4kGPeLKya

- `atlas.html` — the page (styles, markup, search engine, d3 map, chat, request log, activity scores).
- `kb.js` — the knowledge base: entities, facts (definition / moment / decision / number / open / finding), relationships.

The page declares two runtime capabilities when published as an artifact: `db` (request queue,
published findings, per-user activity) and `sample` (ask the ledger). Without them it still
searches and maps.

## Who sees what

`OWNER_EMAIL` at the top of the app script is the only address that sees the Requests and
Activity tabs. Everyone else gets Search, Ask and Map; they can still file a request from the
search results, an entity card, or an unanswered question, and the answer reaches them as an
"additional finding" in search.

The store is split so the page only fetches what the viewer is entitled to:

- `findings` — answers Mike has published. Read by everyone, written only by the owner.
- `requests` — the queue. Written by any viewer filing a request, fetched only by the owner's browser.
- `usage` — per-person time and queries, keyed by email.

Published db rules: root `read: interact / write: owner`, `requests` and `usage`
`interact / interact`, `findings` `read: interact / write: owner`. Rules attach to the published
version that is actually being served, so a share pinned to an older version runs that version's
rules.

To update the index: edit `kb.js`, republish `atlas.html` with `kb.js` as a supporting file.
