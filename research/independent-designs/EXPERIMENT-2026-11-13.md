# Independent sprinkler monitor product engineering comparison — experiment register

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
