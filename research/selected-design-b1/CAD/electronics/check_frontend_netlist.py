#!/usr/bin/env python3
"""Check actual KiCad 10 exported wiring against stored source contract.

This verifies correct net connectivity and source identity. Does NOT qualify
a circuit electrically, evaluate fault energy, or approve a PCB/fabrication.
"""
from __future__ import annotations
import json
from pathlib import Path
from xml.etree import ElementTree

HERE=Path(__file__).resolve().parent
PRJ="B1_24V_FIELD_POWER_REVIEW"
NET_XML=HERE/(PRJ+"_NETLIST.xml")
CONTRACT=HERE/(PRJ+"_net_contract.json")
ERC=HERE/(PRJ+"_ERC.rpt")
def actual_nets():
    doc=ElementTree.parse(NET_XML)
    out={}
    for net in doc.findall(".//nets/net"):
        name=(net.get("name") or "").lstrip("/")
        members=sorted(f"{x.get('ref')}.{x.get('pin')}" for x in net.findall("node"))
        out[name]=members
    return out
def check():
    cfg=json.loads(CONTRACT.read_text())
    nets=actual_nets()
    expected={name: sorted(members) for name,members in cfg["nets"].items()}
    assert set(nets)==set(expected)|{
        "unconnected-(P3-P3_3_NC-Pad3)",
        "unconnected-(P3-P3_4_NC-Pad4)"},(set(nets)-set(expected),set(expected)-set(nets))
    for name,members in expected.items():
        assert nets[name]==members,(name,nets[name],members)
    assert nets["FIELD_PROTECTED_LPLUS"] and "U2.10" in nets["FIELD_PROTECTED_LPLUS"] and "P3.1" in nets["FIELD_PROTECTED_LPLUS"]
    assert set(("P3.2","R5.1")).issubset(nets["SENSOR_I_RETURN"])
    assert "P3.3" not in sum((m for name,m in nets.items() if name.startswith("/")),[])
    assert nets["unconnected-(P3-P3_3_NC-Pad3)"]==["P3.3"]
    assert nets["unconnected-(P3-P3_4_NC-Pad4)"]==["P3.4"]
    assert "U2.5" in nets["RTN_EFUSE_ISOLATED"] and "U2.11" in nets["RTN_EFUSE_ISOLATED"]
    assert "U2.6" in nets["GND_LOGIC"]
    assert set(nets["RTN_EFUSE_ISOLATED"]).isdisjoint(nets["GND_LOGIC"])
    assert set(("R1.1","U1.3","U2.1")).issubset(nets["BOOST_24V"])
    assert set(("R4.1","U2.7")).issubset(nets["ILIM_NODE"])
    assert set(("R4.2","U2.5")).issubset(nets["RTN_EFUSE_ISOLATED"])
    assert set(("J1.1","U1.1")).issubset(nets["PSE_5V_UNVERIFIED"])
    assert all("ADC" not in v["lib_id"] for v in cfg["components"].values()),"Unprotected ADC must not exist in this netlist"
    vals={ref:spec["value"] for ref,spec in cfg["components"].items()}
    assert vals["R4"].startswith("165k"), vals["R4"]
    assert vals["R5"].startswith("100R"), vals["R5"]
    assert vals["U2"]=="TPS26625DRCR_AUTO_RETRY"
    erc=ERC.read_text()
    assert "ERC messages: 0  Errors 0  Warnings 0" in erc,erc[-500:]
    print("B1_KICAD_NETLIST_CONTRACT_PASS",len(cfg["components"]),"components",len(expected),"connected nets, P3 pins 3/4 NC")
    print("B1_ERC_ZERO_REPORTED; DOES_NOT_VERIFY_SURGE_SHORT_POE_ADC_OR_PHYSICAL_HARDWARE")
if __name__=="__main__":check()
