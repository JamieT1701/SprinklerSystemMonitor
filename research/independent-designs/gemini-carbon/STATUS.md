# Gemini Carbon — independent web-model Round 1 response

**Status (2026-11-16):** Owner reports Gemini **4 Carbon** completed in the paid Google Workspace Gemini web app. Coordinator independently found a completed, substantive `Dry-Pipe Sprinkler Monitor Proposal` conversation in the connected browser. The model selector displayed **Carbon** at capture time. This is a **separate model run** from Antigravity CLI `gemini-3.8-flash-high` archived in PR #4.

## Captured evidence

- `round1-browser-rendered-response.txt`: the full **54,919-character page-rendered answer region** obtained from the read-only browser page, preserving visible tables and HTML entity/render artifacts. It is **not a claim of exact raw model-output Markdown bytes**; no direct provider export or execution receipt was available. The web UI displays a complete answer.
- `round1-capture-receipt.json`: provenance and model-certainty limits without publicizing the owner's email address or Gemini conversation URL.
- Prompt: owner was instructed to paste the unchanged Round 1 text from `research/independent-designs/ROUND1-PROMPT.md` (canonical SHA256 `8b46082d7f3cb78569879aedc6144021f0a5dd9c3bed769c8351773b67f5032c`). The browser displays matching opening and closing prompt text; **submitted browser input bytes were not independently hashed**.
- Authentication: paid Workspace Gemini web app, not Antigravity CLI. **Requested/reported/UI model = Gemini 4 Carbon**; exact provider-served model identifier, reasoning internals, token counts and usage cost unavailable.
- Engineering recommendations in the generated report have **not** been independently validated. No production hardware or deployment changes are authorized.

## Competition organization

Keep Carbon's design isolated here, with a **separate draft PR**. Do **not** overwrite Gemini Flash's immutable answer and receipt in PR #4 or Claude's response in PR #5. The coordinator should include three distinct entries in the comparison with explicit evidence-quality notes. Nothing merged or released.

Tracker: https://github.com/JamieT1701/SprinklerSystemMonitor/issues/3

## 2026-11-16 native Google Docs export — complete answer archived

The owner supplied a Google Docs export from the original completed **Gemini 4 Carbon** conversation. It was read through the connected Creative Play Google Drive account and verified to include the complete engineering response (all nine requested sections and tables), not merely the partial browser capture.

- **Preferred complete response:** `round1-google-docs-export.md` — Google Docs **text/markdown export** sliced from its `# **Response: ...` heading through the end **without rewriting** the exported section. UTF-8 length **54,772 bytes**, SHA256 `2e2086e4d021c22c6732b930c22d3a4f4cde6347f0e81fb0bfaa6bfa350bee3f`. Downloaded/verified both locally and independently in the GitHub branch clone.
- **Provenance:** `round1-google-docs-export-receipt.json` records source revision, complete original Google Docs export size/hash, precise extraction boundary, and independent GitHub byte validation. The original full export includes a private Gemini conversation URL and reproduced prompt; only the **response section** was published to the public repository. The Google Doc itself was left untouched.
- The earlier `round1-browser-rendered-response.txt` remains a separate capture for provenance; do not replace the more accurate complete Google Docs export with its DOM rendering.
- **Important distinction:** exact bytes of Google's **exported Markdown response segment** are preserved, but conversion to Google Docs may have changed the native model's original raw Markdown formatting. This is not a provider-native response JSON, cryptographic original input receipt, or proof of the exact model version served.
- Competitor is **Carbon**, not Flash. Gemini Flash's independent CLI results remain in **draft PR #4**; Claude in **draft PR #5**. This branch and **draft PR #6** represent the separate Carbon web response. No designs merged or field systems touched.
