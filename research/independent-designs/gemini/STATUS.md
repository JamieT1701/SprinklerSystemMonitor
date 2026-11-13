# Gemini independent design submission — access checkpoint

**Status (2026-11-13): NOT RUN.** No Gemini model output exists. Do not infer a result from the presence of this branch.

**Identical experiment input:** `research/independent-designs/ROUND1-PROMPT.md` on `research/independent-competition-20261113`, SHA256 `8b46082d7f3cb78569879aedc6144021f0a5dd9c3bed769c8351773b67f5032c`.
**Working branch:** `research/independent-gemini-20261113`.
**Expected source:** Gemini CLI using highest legitimately available reasoning-capable Pro tier; record actual version/model ID/thinking setting and usage in a runtime receipt.

## Access validation
- Arthur: Gemini CLI `0.68.0` executed via `npx -y @google/gemini-cli`. No Gemini CLI OAuth credential configuration or `GEMINI_API_KEY` was available in the current execution environment.
- A minimal test invocation requesting the word `OK` with `-m gemini-2.5-pro` exited with **41**: `Please set an Auth method ...`. **No Gemini inference occurred**.
- Oscar: no installed Gemini CLI or preconfigured `.gemini` directory. This does not prove that the owner lacks a Google account; it only reflects the available CLI environment.
- No API tokens were copied from unrelated Google/GitHub services and no unauthorised paid inference endpoints were activated.

**Unlock condition:** Owner authorizes/signs in to Gemini CLI (Google OAuth) on Arthur, or supplies an authorized model provider connection with transparent cost and model selection. The coordinator then runs the frozen identical Round 1 prompt and commits raw results here, independently of Claude. **Do not replace with simulated Gemini output or another model.**

**Competition index:** [Issue #3](https://github.com/JamieT1701/SprinklerSystemMonitor/issues/3). Do not inspect other advisor outputs before your independent model run is frozen.
