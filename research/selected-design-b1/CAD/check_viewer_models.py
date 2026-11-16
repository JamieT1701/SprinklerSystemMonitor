#!/usr/bin/env python3
"""B1 four-model viewer structural QA (not electrical/mechanical acceptance).

Checks that all four exported GLBs are parseable GLB v2 and contain the
expected compartment/PCB objects. This never tests circuit correctness.
"""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

CAD = Path(__file__).resolve().parent
OUT = CAD / "outputs"

EXPECTED = {
    "B1_concept_interactive.glb": {"case": True, "lid": True, "pcb": True, "sensor": True},
    "B1_lid_off.glb": {"case": True, "lid": False, "pcb": True, "sensor": False},
    "B1_exploded_assembly.glb": {"case": True, "lid": True, "pcb": True, "sensor": False},
    "B1_electronics_only.glb": {"case": False, "lid": False, "pcb": True, "sensor": False},
}
PREFIXES = {
    "case": ("01_Polycarbonate_enclosure",),
    "lid": ("02_Clear_polycarbonate_lid",),
    "pcb": ("20_Main_B1_carrier_PCB",),
    "sensor": ("80_Pressure_transmitter_body",),
}

def load_glb(path: Path) -> tuple[list[str], str]:
    raw = path.read_bytes()
    assert 200_000 < len(raw) < 40_000_000, (path.name, "size range")
    magic, version, declared_len = struct.unpack_from("<4sII", raw)
    assert (magic, version, declared_len) == (b"glTF", 2, len(raw)), (path.name, "bad GLB header")
    chunk_len, chunk_type = struct.unpack_from("<I4s", raw, 12)
    assert chunk_type == b"JSON"
    body = json.loads(raw[20:20+chunk_len].decode("utf-8"))
    names = [node.get("name", "") for node in body["nodes"]]
    assert len(names) >= 60, (path.name, "missing nodes", len(names))
    assert body.get("meshes"), (path.name, "missing mesh data")
    return names, hashlib.sha256(raw).hexdigest()

def main() -> None:
    record = json.loads((OUT / "B1_viewer_variants.json").read_text(encoding="utf-8"))
    assert len(record) == 3
    for filename, flags in EXPECTED.items():
        path = OUT / filename
        assert path.is_file(), filename
        names, hashval = load_glb(path)
        for label, pref in PREFIXES.items():
            observed = any(name.startswith(pref) for name in names)
            assert observed == flags[label], (filename, label, flags[label], observed)
        if filename != "B1_concept_interactive.glb":
            assert record[filename]["bytes"] == path.stat().st_size, (filename, "manifest stale")
        print("VIEWER_MODEL_PASS", filename, "nodes", len(names), "sha256", hashval)

    assert (OUT / "B1_visual_assembly.blend").is_file()
    assert (OUT / "B1_assembled.FCStd").is_file()
    assert (OUT / "B1_complete_reference_assembly.step").is_file()
    print("ALL_FOUR_VIEWER_MODELS_STRUCTURALLY_VALID")
    print("CAUTION: NOT electrical design, fit verification, DRC or product acceptance")

if __name__ == "__main__":
    main()
