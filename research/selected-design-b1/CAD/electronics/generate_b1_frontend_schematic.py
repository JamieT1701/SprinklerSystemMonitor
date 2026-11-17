#!/usr/bin/env python3
"""Generate *real* editable KiCad 10 B1 pressure-loop power schematic.

STRICT SCOPE: schematic for supply/eFuse/field current path ONLY. Not production
PCB, not ADC input protection, not a certified short-safe assembly. Generated
from TI TPS2662 Rev F application note and device pin map.
"""
from __future__ import annotations
import json, uuid, math
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROJECT="B1_24V_FIELD_POWER_REVIEW"
ROOT_UUID="b00b1b10-126e-4444-baaa-0f0000000001"
symbols=[]
instances=[]
wires=[]
labels=[]
no_connects=[]
annotations=[]
contract={"project":PROJECT,"status":"SCHEMATIC_REVIEW_ONLY_NOT_FABRICATION_APPROVED","components":{},"nets":{},"risk_gates":[]}
def uid(tag):
    return str(uuid.uuid5(uuid.UUID(ROOT_UUID),tag))
def esc(s):
    return str(s).replace("\\","\\\\").replace('"','\\"').replace("\n"," ")
def f(x):
    return f"{float(x):.4f}".rstrip("0").rstrip(".")
def prop(k,v,x,y,angle=0,hidden=False):
    return f'(property "{esc(k)}" "{esc(v)}" (at {f(x)} {f(y)} {angle}) (effects (font (size 1.27 1.27)){" (hide yes)" if hidden else ""}))'
def pin(number,name,ptype,x,y,ang):
    return f'''(pin {ptype} line (at {f(x)} {f(y)} {ang}) (length 2.54)
    (name "{esc(name)}" (effects (font (size 1.0 1.0))))
    (number "{number}" (effects (font (size 1.0 1.0)))))'''
def lib_symbol(name,prefix,geo,pins):
    mx=max(abs(x) for x,y,a,b,c,d in pins)+4
    my=max(abs(y) for x,y,a,b,c,d in pins)+4
    rect=f'(rectangle (start -{f(mx-2)} {f(my-2)}) (end {f(mx-2)} -{f(my-2)}) (stroke (width 0.254) (type default)) (fill (type background)))'
    gp= " ".join(pin(str(num),nm,typ,x,y,ang) for x,y,ang,num,nm,typ in pins)
    sym=(f'''(symbol "B1_Bench:{name}"
        (pin_numbers (hide yes)) (pin_names (offset 0.65))
        (exclude_from_sim no) (in_bom yes) (on_board yes) (in_pos_files yes)
        (property "Reference" "{prefix}" (at 0 16 0) (effects (font (size 1.27 1.27))))
        (property "Value" "{name}" (at 0 13.46 0) (effects (font (size 1.27 1.27))))
        (property "Footprint" "" (at 0 0 0) (effects (font (size 1 1)) (hide yes)))
        (symbol "{name}_0_1" {rect})
        (symbol "{name}_1_1" {gp})
    )''')
    symbols.append(sym)
    return {"name":name,"pins":pins}
U2=lib_symbol("TPS26625DRCR","U",None,[
    (-15.24,10.16,180,1,"IN","power_in"),
    (-15.24,5.08,180,2,"UVLO","input"),
    (-15.24,0,180,3,"OVP","input"),
    (-15.24,-5.08,180,4,"SHDN","input"),
    (-15.24,-10.16,180,5,"RTN","passive"),
    (15.24,-10.16,0,6,"GND","power_in"),
    (15.24,-5.08,0,7,"ILIM","passive"),
    (15.24,0,0,8,"dVdT","passive"),
    (15.24,5.08,0,9,"FLT","open_collector"),
    (15.24,10.16,0,10,"OUT","power_out"),
    (0,-15.24,270,11,"PAD=RTN","passive")
])
REG=lib_symbol("U3V9F24_MODULE","U",None,[
    (-10.16,5.08,180,1,"VIN_5V","power_in"),
    (-10.16,-5.08,180,2,"GND","power_in"),
    (10.16,0,0,3,"VOUT_24V","power_out")
])
PORT4=lib_symbol("P3_M12_4F","J",None,[
    (-10.16,7.62,180,1,"P3_1_LOOP_PLUS","passive"),
    (-10.16,2.54,180,2,"P3_2_I_RETURN","passive"),
    (-10.16,-2.54,180,3,"P3_3_NC","passive"),
    (-10.16,-7.62,180,4,"P3_4_NC","passive")
])
# Unlike a passive field plug, this symbol represents the *assumed*
# external, current-limited bench supply attached at J1. The two
# power_out pin types tell ERC an out-of-schematic source is assumed.
# They do NOT prove that Waveshare PoE provides adequate 5V.
PORT2=lib_symbol("EXTERNAL_BENCH_SUPPLY","J",None,[
    (-10.16,2.54,180,1,"ASSUMED_5V_SOURCE","power_out"),
    (-10.16,-2.54,180,2,"ASSUMED_RETURN","power_out")
])
PORT6=lib_symbol("INTERNAL_MONITOR_6PIN","J",None,[
    (-10.16,12.7,180,1,"CURRENT_SHUNT_RAW","passive"),
    (-10.16,7.62,180,2,"GROUND","passive"),
    (-10.16,2.54,180,3,"VBOOST_DIAG_RAW","passive"),
    (-10.16,-2.54,180,4,"FIELD_DIAG_RAW","passive"),
    (-10.16,-7.62,180,5,"3V3_LOGIC","passive"),
    (-10.16,-12.7,180,6,"FLT_RAW","passive")
])
R=lib_symbol("RESISTOR","R",None,[
    (-5.08,0,180,1,"1","passive"),
    (5.08,0,0,2,"2","passive")
])
C=lib_symbol("CAPACITOR","C",None,[
    (-5.08,0,180,1,"1","passive"),
    (5.08,0,0,2,"2","passive")
])
TP=lib_symbol("TESTPOINT","TP",None,[
    (-5.08,0,180,1,"1","passive")
])
def add_instance(lib,ref,value,x,y,netmap,footprint=""):
    # KiCad symbol centers and wire endpoints must align to Eeschema's
    # actual 50 mil (1.27mm) connection grid.
    x=round(x/1.27)*1.27
    y=round(y/1.27)*1.27
    c=uid(ref)
    pins=lib["pins"]
    assert set(netmap)=={str(a[3]) for a in pins}
    inst=f'''(symbol (lib_id "B1_Bench:{lib['name']}") (at {f(x)} {f(y)} 0) (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{c}")
    {prop("Reference",ref,x+4,y-19)}
    {prop("Value",value,x+4,y-16.46)}
    {prop("Footprint",footprint,x,y,hidden=True)}
    {prop("Datasheet","https://www.ti.com/lit/ds/symlink/tps2662.pdf" if ref=="U2" else "",x,y,hidden=True)}
    {''.join(f'(pin "{num}" (uuid "{uid(ref+":"+str(num))}"))' for xx,yy,aa,num,nn,tt in pins)}
    (instances (project "{PROJECT}" (path "/{ROOT_UUID}" (reference "{ref}") (unit 1))))
    )'''
    instances.append(inst)
    contract["components"][ref]={"value":value,"lib_id":lib["name"],"pins":{}}
    for px,py,angle,num,name,ptype in pins:
        net=netmap[str(num)]
        contract["components"][ref]["pins"][str(num)]={"signal":name,"net":net,"type":ptype}
        posx,posy=x+px,y-py
        if net=="NC":
            no_connects.append(f'(no_connect (at {f(posx)} {f(posy)}) (uuid "{uid(ref+"nc"+str(num))}"))')
            continue
        offx=5.08 if px>0 else -5.08
        if px==0:offx=0
        offy=5.08 if py<0 and px==0 else (-5.08 if py>0 and px==0 else 0)
        nx,ny=posx+offx,posy+offy
        wires.append(f'(wire (pts (xy {f(posx)} {f(posy)}) (xy {f(nx)} {f(ny)})) (stroke (width 0) (type solid)) (uuid "{uid(ref+"wire"+str(num))}"))')
        labels.append(f'(label "{esc(net)}" (at {f(nx)} {f(ny)} 0) (effects (font (size 1.0 1.0)) (justify left bottom)) (uuid "{uid(ref+"net"+str(num))}"))')
        contract["nets"].setdefault(net,[]).append(f"{ref}.{num}")
# Group by source, current limit, M12, monitor header; connected through explicit labels
add_instance(PORT2,"J1","BENCH_5V_SOURCE_ASSUMED_NOT_VALIDATED",40,60,{"1":"PSE_5V_UNVERIFIED","2":"GND_LOGIC"})
add_instance(REG,"U1","Pololu_5588_NOT_SHORT_PROOF",75,61,{"1":"PSE_5V_UNVERIFIED","2":"GND_LOGIC","3":"BOOST_24V"})
add_instance(U2,"U2","TPS26625DRCR_AUTO_RETRY",176,93,{"1":"BOOST_24V","2":"UVLO_NODE","3":"OVP_NODE","4":"ENABLE_3V3","5":"RTN_EFUSE_ISOLATED","6":"GND_LOGIC","7":"ILIM_NODE","8":"DVDT_NODE","9":"EFUSE_FAULT_N","10":"FIELD_PROTECTED_LPLUS","11":"RTN_EFUSE_ISOLATED"},footprint="")
add_instance(PORT4,"P3","M12_A4_Female_SPTD25_1+_2RETURN",268,89,{"1":"FIELD_PROTECTED_LPLUS","2":"SENSOR_I_RETURN","3":"NC","4":"NC"})
# TI Figure 10-1: 715k IN->UVLO, 20k UVLO->OVP, 30.1k OVP->RTN
add_instance(R,"R1","715k_1pct_UV_TOP",85,115,{"1":"BOOST_24V","2":"UVLO_NODE"})
add_instance(R,"R2","20k_1pct_UV_MID",85,128,{"1":"UVLO_NODE","2":"OVP_NODE"})
add_instance(R,"R3","30.1k_1pct_OV_BOTTOM",85,141,{"1":"OVP_NODE","2":"RTN_EFUSE_ISOLATED"})
add_instance(R,"R4","165k_1pct_THEORY_40mA",224,155,{"1":"ILIM_NODE","2":"RTN_EFUSE_ISOLATED"})
add_instance(C,"C1","10nF_50V_DVDT",224,167,{"1":"DVDT_NODE","2":"RTN_EFUSE_ISOLATED"})
add_instance(C,"C2","1uF_50V_BOOST_INPUT",85,154,{"1":"BOOST_24V","2":"GND_LOGIC"})
add_instance(C,"C3","1uF_50V_FIELD_OUTPUT",224,178,{"1":"FIELD_PROTECTED_LPLUS","2":"GND_LOGIC"})
add_instance(R,"R5","100R_0.1pct_0.25W_SHUNT",290,155,{"1":"SENSOR_I_RETURN","2":"GND_LOGIC"})
add_instance(R,"R6","100k_FLT_PULLUP",224,191,{"1":"LOGIC_3V3","2":"EFUSE_FAULT_N"})
add_instance(R,"R7","10k_ENABLE_PULLUP",224,204,{"1":"LOGIC_3V3","2":"ENABLE_3V3"})
add_instance(PORT6,"J2","RAW_INTERNAL_MONITOR_NO_ADC_CLAMP",317,97,{"1":"SENSOR_I_RETURN","2":"GND_LOGIC","3":"BOOST_24V","4":"FIELD_PROTECTED_LPLUS","5":"LOGIC_3V3","6":"EFUSE_FAULT_N"})
# test points not a current-limiting/surge protection mechanism
add_instance(TP,"TP1","FIELD_24V",291,194,{"1":"FIELD_PROTECTED_LPLUS"})
add_instance(TP,"TP2","RAW_SHUNT_0_TO_FAULT",291,207,{"1":"SENSOR_I_RETURN"})
add_instance(TP,"TP3","EFUSE_RTN_NOT_GND",291,220,{"1":"RTN_EFUSE_ISOLATED"})

def textnote(s,x,y):
    annotations.append(f'(text "{esc(s)}" (at {f(x)} {f(y)} 0) (effects (font (size 1.52 1.52)) (justify left bottom)) (uuid "{uid("note"+s)}"))')
textnote("B1 COMMERCIAL PROTOTYPE / REAL KICAD 10 CONNECTIVITY / NOT FABRICATION READY",28,21)
textnote("TI TPS26625: RTN and GND MUST NOT BE DIRECTLY SHORTED (reverse polarity protection)",26,30)
textnote("FIELD LOOP: SPTD25 P3 pin 1=limited 24V; pin 2=return; pins 3/4 NC",26,38)
textnote("FRONTEND PROTECTION INCOMPLETE: J2 RAW SIGNALS NEVER CONNECT DIRECTLY TO ADS1115",26,239)
textnote("LIMIT R4 165k => 40.2mA nominal by TI formula. Tolerance/short heating UNQUALIFIED.",26,247)
textnote("BOOST U1 Pololu 5588 NOT SHORT PROTECTED. PoE 5V POWER/STARTUP UNVERIFIED.",26,255)
textnote("C2/C3/FLT/SHDN values and interdomain faults require independent bench validation.",26,263)
textnote("24V backfeed, RTN excursions, ESD/TVS, rail discharge, ADC powered-off clamp: NOT DESIGNED",26,271)
textnote("J1 power-output pin types are EDA SOURCE ASSUMPTIONS; NOT validated hardware!",26,279)
contract["risk_gates"]=[
 "24V backup/PoE budget unverified; Pololu 5588 is not short-circuit tolerant",
 "eFuse 165kΩ current limit is a calculated target only; 40mA tolerance and thermal auto-retry not measured",
 "Separate RTN and GND modeled; not a proven PCB return/reverse-fault strategy",
 "No TVS/cable ESD/connector wet ingress, powered-off ADC input clamp or power-rail backfeed isolation",
 "J2 is RAW MONITORING boundary; do NOT attach ADS1115 to 24V raw inputs or directly to 4V shunt on short",
 "P3 contact numbering verified against ProSense datasheet, physical cable continuity yet to measure",
 "No actual system connection, PCB routing, DFM, IEC/IP testing or fabrication released",
 "PoE power/logic EN pullup behavior and fault pin tolerance unverified",
 "C3 and device output/thermal startup under short require measurement",
 "No site-side pressure tap/range approved",
 "J1 source-pin directions are external bench-power assumptions only, NOT proof of PoE capacity",
]
sch=f'''(kicad_sch (version 20260101) (generator "eeschema") (generator_version "10.0")
 (uuid "{ROOT_UUID}") (paper "A3")
 (title_block (title "B1 24V pressure-loop power path - UNQUALIFIED") (date "2026-11-16") (rev "B1-SCH-01") (company "Device Lab bench design; not field use"))
 (lib_symbols
 {chr(10).join(symbols)}
 )
 {chr(10).join(wires)}
 {chr(10).join(labels)}
 {chr(10).join(no_connects)}
 {chr(10).join(annotations)}
 {chr(10).join(instances)}
 (sheet_instances (path "/" (page "1")))
 (embedded_fonts no)
)'''
out=HERE/(PROJECT+".kicad_sch")
out.write_text(sch,encoding="utf-8")
(HERE/(PROJECT+"_net_contract.json")).write_text(json.dumps(contract,indent=2)+"\n",encoding="utf-8")
# Install authentic project-local symbol library, so KiCad validates pin IDs
# against the same names and coordinates embedded in the schematic.
libdoc='(kicad_symbol_lib (version 20251024) (generator "kicad_symbol_editor") (generator_version "10.0")\n'
for entry in symbols:
    libdoc += entry.replace('(symbol "B1_Bench:','(symbol "')+"\n"
libdoc += ')\n'
(HERE/"B1_Bench.kicad_sym").write_text(libdoc,encoding="utf-8")
(HERE/"sym-lib-table").write_text(
    '(sym_lib_table (version 7) (lib (name "B1_Bench") (type "KiCad") (uri "${KIPRJMOD}/B1_Bench.kicad_sym") (options "") (descr "Device Lab B1 preliminary engineering symbols")))\n',
    encoding="utf-8")
print("KICAD_B1_SCHEMATIC_CREATED",out.name,len(symbols),"embedded symbols",len(instances),"real components",len(wires),"wires",len(contract["nets"]),"nets")
