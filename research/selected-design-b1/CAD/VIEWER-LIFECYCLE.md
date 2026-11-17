# B1 permanent interactive viewer — publishing and maintenance contract

**Status:** retained as the designated **living B1 engineering visual review**; the web address remains stable while the CAD evolves. Updated 2026-11-16.

## Permanent address and ownership

- **Viewer:** https://jamiet1701.github.io/SprinklerSystemMonitor/b1-viewer.html
- Deep links: `?view=closed`, `?view=lid`, `?view=exploded`, `?view=electronics`
- Web page source: `docs/b1-viewer.html` on the GitHub Pages publishing branch **`docs/device-lab-2026-11-10-checkpoint`**.
- **Current editable CAD and GLB authority:** `research/selected-design-b1/CAD/` on the B1 engineering branch **`design/claude-b1-engineering-20261116`**; tracked through draft PR #7. This is not the production R6 branch.
- Source model URLs are intentionally **branch-based, not pinned to an old commit**. The existing viewer page loads the latest committed GLB assets from that branch each time it opens (browser query-string cache bust on new page load). Published models **are not automatically regenerated from FreeCAD or Blender source**.
- The stable site is a **visual engineering demonstration**, not a connected operational dashboard, a certified safety device, or a fabrication release.

## The four retained, distinct models

| Mode | GLB in `CAD/outputs/` | Purpose |
|---|---|---|
| Closed | `B1_concept_interactive.glb` | Complete housing, illustrative cables and external sensor bodies |
| Lid Off | `B1_lid_off.glb` | Remove the lid, seal, screws and lid labels; inspect PCB within box |
| Exploded Assembly | `B1_exploded_assembly.glb` | Separate lid and carrier vertically to reveal assembly structure |
| Electronics Only | `B1_electronics_only.glb` | Remove case and external sensors for PCB and module inspection |

These are separate GLB geometries derived from the **same** Blender source scene and FreeCAD geometry, not an unsafe claim to full disassembly, native KiCad net connectivity or real manufacturer-clearance verification.

## Required process for each future mechanical/electronics revision

1. Make CAD modifications in the **B1 engineering branch**. Re-check current `AGENTS.md` or other applicable governance on the authoritative target branch and verify the current PR before consequential changes. Reuse `B1_dimensions.json` as the geometry contract.
2. Regenerate FreeCAD native solid/STEP/meshes using `b1_freecad.py`; regenerate material/camera scene/renders using `b1_blender.py`. If geometry was only edited within Blender, document the divergence and reconcile it back into the FreeCAD/source model.
3. Re-export the closed `B1_concept_interactive.glb` using `b1_export_glb.py`, then **all three additional internal views** using `b1_export_assembly_variants.py`. Never update only the closed model while leaving the internal views stale.
4. Run `check_viewer_models.py`, the host-only test suite, and `b1_bundle.py` to refresh the model integrity record and full download archive. If a new source document/script is added, include it in the full archive and recalculate `B1_FULL_DESIGN_CONCEPT_SHA256.txt`.
5. **Visual QA is mandatory:** Open the browser viewer or a locally served copy and inspect each of Closed, Lid Off, Exploded and Electronics Only. Specifically check label transforms, visibility, geometric overlap, module placement, and whether component/model numbers are labeled provisional where appropriate.
6. Commit reviewed GLB assets, source code, native CAD, renders, test evidence and package checksum to the B1 engineering branch. Maintain draft PR #7 (or successor if scope evolves) with changes and honest maturity status. The existing viewer URL will then point to the updated branch files; **refresh the page** to pick up current models after GitHub Raw caches clear.
7. If the model source branch is merged, renamed, or deleted, **repoint the website's four model URLs to a permanent live target first**, verify all four deep links publicly, then retire the old branch. Never leave the public site pinned to a deleted source branch. No new page or URL is needed.

## Model generation (Arthur, Ubuntu)

```sh
cd /home/jamiet1701/.local/share/device-lab-advisor-competition/engineering-b1/research/selected-design-b1/CAD
flatpak run --user --filesystem="$PWD" --command=FreeCADCmd org.freecad.FreeCAD "$PWD/b1_freecad.py"
flatpak run --user --filesystem="$PWD" --command=blender org.blender.Blender --background --factory-startup --python "$PWD/b1_blender.py"
flatpak run --user --filesystem="$PWD" --command=blender org.blender.Blender --background --factory-startup --python "$PWD/b1_export_glb.py"
flatpak run --user --filesystem="$PWD" --command=blender org.blender.Blender --background --factory-startup --python "$PWD/b1_export_assembly_variants.py"
python3 check_viewer_models.py
python3 b1_contact_sheet.py
python3 b1_bundle.py
cd ..
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s VERIFICATION -p 'test_*.py' -v
```

Only rerun CAD modeling when source geometry has changed; when preparing a viewer-only change, it is safe to validate the existing files without rebuilding them. FreeCAD Blender KiCad are all free and already installed on Arthur.

## Release boundary

A rendering that looks electrically complete is **never** evidence of a completed circuit. Future schematic, PCB, sensor, connector and mechanical enclosure changes must remain labeled unverified until their own applicable schematic review, KiCad ERC/DRC, mechanical fits, fault-tolerant bench tests and site approvals pass. Preserve working sprinkler R6 hardware and firmware under its own governance; no field system changes from this viewer work.

## Publication check

1. Viewer site returns HTTP 200.
2. All four GLB URLs return HTTP 200 and `access-control-allow-origin: *` from public GitHub Raw.
3. Deep links `?view=lid`, `?view=exploded`, `?view=electronics` each generate `data-b1-model-ready=true` in an actual browser (not merely a valid file URL).
4. Viewer controls switch models, reset/orbit works, release disclaimers remain, and the current design revision has been documented on PR #7.
5. Report only verified results. Do not claim that changing source code updates the viewer until the exported GLB and published model URLs are updated.

### Rev B connection changes: visual review policy

Connector redesign lives in source-controlled FreeCAD \`b1_freecad.py\` and \`B1_dimensions.json\`; all four GLBs must be regenerated and published together after review. Confirm the user sees **plug-in PoE / TEMP M8 / PRESS M12** in Closed + Lid Off, physical bulkheads remain attached to case in Exploded, and Electronics Only hides external sockets. AUX marker is a **solid wall**, not a new field connector. Reproduce the connector port geometry test, inspect \`05_b1_field_ports.png\`, then record residual fit/ingress/PoE gates; preview is **not** an approved installation.

### Pressure sender CAD source and identity

The model candidate is **SPTD25-20-0100H** and envelope diameter 18.9mm / total length 66.9mm from its supplier drawing, with approximate caps/hex/threads. As model and supplier MPN change, update `B1_dimensions.json`, FreeCAD source and all four viewer exports **together**. DFM must independently obtain true manufacturer STEP and physical vendor part before fabrication. Pressure output remains 2-wire 4-20mA at P3 pin1 + / pin2 return, other contacts NC.
