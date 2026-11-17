# Independent sprinkler monitor product engineering comparison — experiment register

> **FINAL ROUND 1 STATUS (2026-11-17): COMPLETE AND FROZEN.** Three original independently produced model submissions have been preserved in separate unmerged draft PRs [#4](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/4), [#5](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/5), [#6](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/6); source fidelity and limits are recorded. The unchanged six-category rubric was applied in [COMPARISON.md](./COMPARISON.md), with critical design defects in [TECHNICAL-AUDIT.md](./TECHNICAL-AUDIT.md). **Claude Opus 5.5** was selected as a **future engineering direction (82/100)**, not fabrication or field approval. Round 1 coordinator Issue #3 was closed as completed on Nov 17; follow-on B1 research remains in Issue #2 and draft PR #7. **Earlier entries below saying “Claude pending” or “comparison gate not met” are chronological history and no longer current.** Do not rewrite raw model proposals or delete their source branches.


**Date:** 2026-11-13 (owner requested design competition)
**Coordinator:** ChatGPT, using owner-authorized GitHub and Desktop Commander only.
**Experiment issue:** https://github.com/JamieT1701/SprinklerSystemMonitor/issues/3
**Canonical clean-room functional brief:** `research/independent-designs/BRIEF.md`
**Identical Round 1 prompt:** `research/independent-designs/ROUND1-PROMPT.md`
**Input SHA256 (UTF-8 bytes):** `8b46082d7f3cb78569879aedc6144021f0a5dd9c3bed769c8351773b67f5032c`
**Isolation:** AI providers receive only the identical brief and Round 1 instructions. No repository access, no tools, no existing prototype files, no access to competing answers. Coordinator commits raw outputs to GitHub **only after** the individual run completes.

## Models and state

| Advisor | Branch / output location | Model selection / reasoning | Source / authentication | Result |
|---|---|---|---|---|
| Claude | `research/independent-claude-20261113`, `research/independent-designs/claude/` | Claude Code CLI `--model opus --effort max`; runtime should report exact served model | Claude Code installed and authenticated with existing user subscription on Arthur; isolated temporary working directory, tools disabled, no session persistence | **Launched; output pending verification** |
| Gemini | `research/independent-gemini-20261113`, `research/independent-designs/gemini/` | Gemini CLI highest available Pro/reasoning once authenticated, exact model must be verified | Gemini CLI 0.68.0 available via temporary npx on Arthur; **no Gemini authentication configured**; login test returned exit code 41 | **BLOCKED — never claim run/completed** |

### Reproducibility and privacy

- Run the same `ROUND1-PROMPT.md` byte-for-byte with a model adapter; preserve raw vendor response, actual model and reasoning setting, CLI invocation/options, run date and exit code. Do not publish credentials or OAuth/session tokens.
- Claude CLI is isolated in `/tmp/device-lab-advisor-competition/claude`, invoked with `--tools '' --disable-slash-commands --no-session-persistence`; no repo access is granted to the model.
- Gemini CLI test asked only for `OK` and produced **no model answer**; local environment lacks `~/.gemini` credentials and `GEMINI_API_KEY` / `GOOGLE_GENAI_USE_VERTEXAI` / `GOOGLE_GENAI_USE_GCA` were unset. Requires owner sign-in or authorized configured provider. Do not substitute another model and mislabel it Gemini.
- Archive transcript/response only after model succeeds. Separate branches make results durable but GitHub does not technically prevent a future model from browsing another branch; isolation is ensured by model invocation and tools disabled.
- Keep this experimental work separate from current hand-built monitor, existing R6 prototype branch and any production equipment or sensors. Do not change system, deploy firmware, incur material spending, invite partners or order hardware as part of comparison.

## Scoring criteria (after both raw submissions frozen)

| Criterion | Weight |
|---|---:|
| Fault tolerance, measurement trustworthiness and reliability | 25% |
| Solo-workshop repeatable build / test feasibility | 20% |
| Unit economics + operation/alert/support costs | 20% |
| Engineering specificity and design completeness | 15% |
| Installation and field serviceability | 10% |
| Compliance, cybersecurity and commercial readiness | 10% |

Score evidence, not apparent complexity or model brand. Penalize unsupported accuracy, protection, system trip thresholds, certification, material prices or cost/production claims. Ask the same follow-up interview question across advisors when practical.

## TODO

- [ ] Claude actual result verified and exact original response committed to its branch.
- [ ] Obtain a real Gemini login/model path using an authorized connection; rerun the same input and archive result.
- [ ] Store vendor/version/effort and hash receipts per advisor; if model falls back, disclose.
- [ ] Freeze independent proposals before comparative assessment.
- [ ] Prepare `COMPARISON.md` only when both are available; do not treat an unrun model as equivalent to a completed proposal.
- [ ] Run deeper design rounds and owner interviews as appropriate with separate durable records and revised questions logged.

**No final product selection, PCB fabrication output, pressure sensor acceptance or safety/commercial approval is implied by this experiment.**


## November 16, 2026 checkpoint — Gemini frozen, Claude outstanding

**Current state overrides the historical November 13 model-status table above.** Arthur came back online after the prior temporary Claude run directory was lost; the prior run was **not** verified completed. Both advisors received the exact same frozen 12,484-byte prompt (SHA256 `8b46082d7f3cb78569879aedc6144021f0a5dd9c3bed769c8351773b67f5032c`), without the prototype or peer output.

- **Gemini completed 2026-11-16 15:04:51 America/New_York** via authenticated Google Antigravity CLI 1.5.9 (legacy Gemini CLI personal login had been retired). Only Gemini 3.8 Flash High/Medium/Low appeared in the available model list; highest available `gemini-3.8-flash-high` was used, **not a Pro model**. User-approved OAuth sign-in succeeded, round returned exit 0 / status SUCCESS, 4,837-word original text. Input *argument* hash matched exactly, so round was truly same prompt. No served model ID was in result JSON. Raw public-facing text was preserved unedited, SHA256 `38ae82b1452c5f0653bf12b35da058c20a1748fb0bdabc34753925754fe08a63`. **GitHub freeze:** `research/independent-gemini-20261113` commit [b1aa7e7](https://github.com/JamieT1701/SprinklerSystemMonitor/commit/b1aa7e77c8bb30c23d9a1bbeb696d85476aa1c31), [draft PR #4](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/4). The original report and sanitized receipt are in `research/independent-designs/gemini/` on that branch.
- **Claude restarted 2026-11-16 14:50 America/New_York**, verified CLI running authenticated `--model opus --effort max --tools '' --disable-slash-commands --no-session-persistence`, persistent local artifacts under `/home/jamiet1701/.local/share/device-lab-advisor-competition/claude/`. As of 15:06, still active, **no response or exit code**. Do not interpret active PID as successful inference; do not relaunch or score before reviewing original output and receipt.
- **Recovery mechanism:** one-time assistant automation scheduled for approximately 15:25 America/New_York to recheck verified Arthur output and continue GitHub archival only if completed. Not a guarantee that a model completes or a persistent inference service. Original unverified Claude run and Gemini authentication blocker from November 13 are historical, not the latest state.
- **Comparison gate:** no final scoring, independent review or winner selection until Claude and Gemini verified proposal+receipt are frozen on distinct branches. Keep both draft PRs unmerged. No physical prototype, firmware, sprinkler, customer or procurement changes authorized by this competition.


## 2026-11-16 correction — third web Gemini Carbon entry

**Owner correction:** Gemini 4 Carbon was used via the paid Google Workspace Gemini web app. The previous two-entry comparison inventory omitted the completed Carbon web run; the earlier Antigravity **Gemini 3.8 Flash High** CLI run remains real and separately archived. There are now **three candidate reports**:

| Advisor | GitHub evidence | Fidelity and model provenance |
|---|---|---|
| Claude Opus 5.5 (max effort CLI) | [draft PR #5](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/5), commit `c0421d8` | Verified served model ID in provider response; actual success; model public-facing response preserved verbatim |
| Gemini 3.8 Flash High (Antigravity CLI) | [draft PR #4](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/4), commit `b1aa7e7` | Requested Flash High CLI; actual success; native response preserved verbatim; served ID not supplied |
| Gemini 4 Carbon (paid Workspace web app) | [draft PR #6](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/6), commit `e6773dea` | User confirms Carbon and browser picker showed Carbon when read; full browser-rendered output region archived, **not a byte-identical native export or runtime receipt**; exact served version and original submitted prompt bytes unverified |

The web Carbon proposal came from a completed standalone Gemini chat with a clean-room Round 1 prompt. Its response was captured with an authorized read-only browser tab tool and persisted under `research/independent-designs/gemini-carbon/` on `research/independent-gemini-carbon-20261116`. No existing competitor answer was passed into the web chat. The UI evidence supports user-reported Carbon, but does not establish a versioned provider execution receipt; comparisons must label the capture limitation.

**Revised gate:** Score three entries using the unchanged rubric. Prior two-entry comparative instructions are superseded. No additional model calls, merging, product orders, field/firmware changes, or commercial action implied. Issue #3 records the correction.


## Source-fidelity upgrade — Gemini Carbon Google Docs export (2026-11-16)

The owner supplied a complete exported Google Doc of the **paid Workspace Gemini 4 Carbon** Round 1 response. The authoritative text for **Carbon design comparison** is now the complete [Google Docs Markdown export](https://github.com/JamieT1701/SprinklerSystemMonitor/blob/research/independent-gemini-carbon-20261116/research/independent-designs/gemini-carbon/round1-google-docs-export.md) on [draft PR #6](https://github.com/JamieT1701/SprinklerSystemMonitor/pull/6). It contains all nine Round 1 sections and engineering tables, **54,772 UTF-8 bytes**, SHA256 `2e2086e4d021c22c6732b930c22d3a4f4cde6347f0e81fb0bfaa6bfa350bee3f`, independently reverified against a clone of the GitHub branch. See the branch's `round1-google-docs-export-receipt.json` for source export SHA256, source revision and exact extraction boundaries.

This supersedes **Carbon's earlier browser-rendered text as the preferred report**, while leaving it archived for provenance. Only the response portion of the Google Docs export was published; the original document's private Gemini URL and reproduced prompt preamble are not in the public GitHub response file. The Google Doc was not modified. **Format caveat:** Google Docs Markdown conversion may differ from the raw model output; there is no provider-native raw Carbon run/usage receipt. It is distinct from Gemini Flash High CLI PR #4 and Claude Opus 5.5 PR #5. All PRs remain draft and unmerged; research-only, no production or sprinkler system changes.
