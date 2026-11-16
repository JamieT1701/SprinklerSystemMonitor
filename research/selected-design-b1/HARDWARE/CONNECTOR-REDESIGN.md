# B1 Revision B — external service connectors and measured expansion headroom

**Engineering design change candidate — 2026-11-16**
**State:** selected for **editable concept CAD**, **not a completed electrical schematic / routed PCB / IP-certified product**. Applies only to commercial B1 design branch. The existing live R6 is untouched.

## Outcome

All ordinary field connections plug in **from the exterior**. The lid stays closed for PoE cable, pressure transmitter, and DS18B20 probe swaps; internal PCB terminals may remain as **factory/service wiring** only. No exposed threaded plumbing NPT penetration is needed in the *electronic enclosure*: the remote industrial pressure transmitter's **process** fitting remains an installer-approved NPT (or other) process tap on an approved air-pressure domain; its *electrical* signal travels through a cordset to a panel M12.

### The three production connector ports

| ID | External connector (mating side) | Proposed part / family | Function | Cable/installation approach | Maturity |
|---|---|---|---|---|---|
| **P1** | Female shielded **Cat5e RJ45 feedthrough**, industrial protected bulkhead, with proper mated shroud or cap | **Amphenol LTW RCP-5SPFFH-SCM7002** *candidate*, or equivalent vendor with PoE testing | **Ethernet + 802.3af PoE** to internal factory Waveshare RJ45 | Standard short shielded internal RJ45 patch cord and qualified external Ethernet lead; IP67 claim only if **mated with compatible sealed assembly** (or capped when unplugged) | Candidate supplier MPN **not PoE current/EMC qualified yet** |
| **P2** | **M8 A-coded 3-contact female** screw/snap panel mount | **binder 76 6518 1111 00003-0200**, IP67/IP69K family, manufacturer M12x1 front mount | **DS18B20 3-wire ambient probe** | Factory-molded matching **male M8**, cable strain relief, three-wire probe with 3.3V excitation and field ESD/CRC | Candidate with **pin designation and actual cable** pending |
| **P3** | **M12 A-coded 4-contact female** screw-coupled panel mount | **binder 76 4332 0011 00004-0200**, M16x1.5 female, IP67 | **Single 2-wire 4–20mA industrial air-pressure transducer** | Prewired matching **male M12** on B1 side; sensor end connector determined by selected transmitter's real interface; two unused poles insulated / not live | Candidate; qualified sensor MPN/process location pending |

These three **different** external connector form factors make accidental swapping of Ethernet, 3.3V 1-Wire and 24V loop cables mechanically impossible. Bulkhead field sockets are **female** on the equipment to minimize accessible energized pins; the matching removable cord ends are **male** at this enclosure, but remote transducers may have their own manufacturer connector and require a suitable cable assembly. Verify actual gender/compatibility with selected cable drawings.

**Do not insert a common generic GX12/GX16 'aviation connector' into the B1 release by appearance alone.** A scale may indeed use such a connector, but the user's exact connector has not been identified. It could be acceptable with a genuine identified ingress rating, mating cycles and supply chain; M8/M12 offers stronger published interoperability and sourcing. Send a photo or scale model for future comparison if it materially changes manufacturing cost.

### Provisional electrical function map — NOT an orderable harness pinout

| Field port | Electrical roles | Caveat |
|---|---|---|
| P1 RJ45 | Ethernet differential pairs and PoE pass-through, identical pin-to-pin across a verified shielded coupler | External component/lead must be tested with live 802.3af PSE/PD and full-load startup; don't assume any generic 8P8C adapter's PoE/EMI performance |
| P2 M8 3-contact | +3.3V **after field protection**, 1-Wire DATA, return GND | **Manufacturer-specific contact numbering unassigned** until female panel and male cordset drawings are reconciled; protect power-off pin injection/ESD |
| P3 M12 4-contact | Protected hardware-limited +24V loop source, 4–20mA sensed return; **two remaining poles NC** | Proposed common industrial mapping *M12 pin 1 = supply / pin 3 = return* requires confirmation against actual transmitter and harness. Never expose unprotected 24V or assume arbitrary pressure sensor polarity. |

**Hot plug:** All connector mates must be safe when the external cable is inserted/removed while the **device power is present**, but this requires rated connector procedures, proper hardware current limit and debounce/recovery proof. The candidate binder datasheet warns against unplugging under load; **do not approve routine live hot-swapping until the exact mating pair is tested and manufacturer limits are reconciled**. An installer can isolate PoE power before sensor swaps during early pilots.

## Dust, moisture and serviceability target

- Candidate enclosure is Hammond 1554T2GYCL clear-lid polycarbonate; preserve its original gasket and screw fastening. The actual **modified enclosure** IP rating is not established by any CAD model.
- Target **IP54** minimum after controlled enclosure/cable assembly tests for intended sheltered riser-room locations, optional **IP65** stretch only after gasket, penetrations and cable sealing qualify. No claims of waterproof/dustproof merely because an M8/M12 part is sold as IP67.
- Each mated/capped interface must match manufacturer's specific mating/cap part and install tightening guidance. Unmated exposed RJ45 with a generic nonsealed patch cable **does not satisfy IP67**.
- Place all three **downward-oriented** ports on the same low short end wall to allow gravity drip loops and accessible service; do not mount electrical outlets under an active leak or spray path. Keep pressure probe remote from cabinet.
- Planned concept hole diameters: RJ45 **20.8 mm** (Amphenol dimensional candidate D-cut), M8 **12 mm** (manufacturer M12x1 external mount), M12 **16 mm** (manufacturer M16x1.5 external mount). **Final cut-outs are manufacturer-print-dependent**, not drill instructions.
- The nominal enclosure front wall in our model is ~3.94 mm thick; Amphenol candidate with protective cap nominally permits **≤3.0 mm local panel thickness**. One **local internal spotface** is represented only as an engineering placeholder; actual OEM mold wall/boss integrity must be checked before drilling.
- Verify **full connector overmold and nut clearance**, rear RJ45 internal patch-cord bend radius, rear pressure/temp pigtail service loops, panel wall spacing, plastic fracture and ingress testing. **External 120mm end-wall** is tight: 38mm Ethernet coupling OD next to M8/M12; stop release on collision.
- Source cost note: supplier-listed Amphenol RJ45 coupler around **$9.97 single** (Nov 2026 search; price not negotiated), compared to >$90 listed Bulgin Buccaneer; the compatible sealing mating assembly may add material cost. No commitment or purchase made.

## Expandability without unnecessary connectors

**B1 Rev B release hardware has exactly 3 populated external service ports.** On the **right long wall** reserve a CAD-designated **AUX BLANK**, with **no hole, wiring, powered header, exposed contacts, or additional PCB fault path**. The first commercial concept does not need a fourth plug.

Potential later sensor priorities:

| Future sensor | Useful? | Relative effort | Decision |
|---|---|---|---|
| **Second room / pipe-adjacent air temperature probe** (independent DS18B20 bus and separate M8 port) | **Most practical** for a second remote temperature location; helps distinguish localized cold, not a replacement for measured pipe freezing | **Low/moderate**: another GPIO, input ESD, connector and cable, separate fault quality and dashboard | **First expansion candidate**, activate only if pilot placement reveals a true need |
| **Second system-side pressure channel** | Valuable only for another actual independent pressure domain | **High**: additional isolated/limited 24V source channel, current sensing/diagnostics, analog channel resources and inter-channel fault analysis | Prefer **second B1 device**, not multi-sensor current-loop expansion |
| **Ambient relative humidity** | Context for condensation risk or sensor cabinet environment | **Low** if inside box, but **inside box != true riser-room ambient**; external sensor requires another sealed port | Defer pending measured need |
| **Passive floor water leak indicator** | Detects flooding / water accumulation not necessarily pressure loss | Moderate: water sensor survivability, false positive handling and cable entry | Optional facility feature, not B1 core |
| **Compressor motor status/current sensing** | Can help diagnose compressor cycling vs air loss | **High**: qualified external CT/installation, power systems exposure and additional signal processing | Separate later product lane; do **not** add mains wiring to B1 |
| **Enclosure temperature/self-test** | Can identify electronics overheating | **Low**, onboard IC or MCU data | Firmware/internal expansion candidate; no field connector needed |

**Do not turn the spare into a 'universal powered sensor' without actual EMC, ESD, power budget and field cable requirements.** Optional industrial RS-485 may be considered only if a paid customer/field requirement exists; reserve space, not functional promises.

## Exact preliminary module positioning (for public viewer only)

- Existing 120×180×90.5mm nominal envelope.
- Three panel port axes **X = -35mm / 0mm / +35mm**, short-front wall **Y=-90mm**, Z≈**35mm** (subject to cable/PCB spatial collisions).
- Reserved AUX location on side wall near X=+60, Y≈+20, Z≈37mm, **visual marker but NO CUTOUT**.
- Original internal screw terminals may remain as **factory-only** PCB service terminations. Field wiring must terminate at the bulkhead connector and stay serviceable without opening the lid.
- Rendering dimensions for connector shells are **illustrative** until exact OEM STEP/CAD is imported; look at the published viewer for fit concept, never use its geometry directly as a drill jig.

## Unresolved manufacturer / acceptance gates

1. Verify exact MPNs, genuine datasheets, matching male cordsets, true cut-outs/board clearances, complete cost and stock at 1/5/25/100 units.
2. **PoE load test** through the RJ45 feedthrough, external sealed mating cable, internal patch cable, after normal shield/ground layout choice and -20..+70C component limits.
3. Wiring/harness and pin mapping independently checked against real industrial 4–20mA transmitter and DS18B20 probe. Label pressure harness explicitly; avoid assumptions about standard wire colors.
4. Both sensor interface circuits survive swapped/shorted/opened/wet cable, reverse insertion attempt, 24V miswire and **ADC unpowered**; output 24V limit remains hard design blocker.
5. OEM exact STEP and physical fit, wall thickness/recess/fastener validation; thermal/condensation, impact, washdown and strain relief.
6. End-to-end correct fault/stale alert propagation while unplugging **during bench testing** (no in-service sprinkler system).
7. Mechanical and environmental acceptance by intended installation class; no claim of certified IP54/IP65 until independently tested.

## Manufacturer / vendor records

- [Amphenol LTW RCP-5SPFFH-SCM7002 RJ45 sealed Cat5e panel coupler — DigiKey](https://www.digikey.com/en/products/detail/amphenol-ltw/RCP-5SPFFH-SCM7002/7619820)
- [binder M12 A 4-pole female M16x1.5 panel connector](https://www.binder-usa.com/us-en/products/automation-technology/m12-a/76-4332-0011-00004-0200-m12-a-female-panel-mount-connector-4-unshielded-single-wires-ip67-ul-m16x15)
- [binder M8 A 3-pole female panel connector](https://www.binder-connector.com/en/products/automation-technology/m8/76-6518-1111-00003-0200-m8-female-panel-mount-connector-contacts-3-unshielded-single-wires-ip67-ip69k-ul-m12x10-front-fastened)
- [Bulgin PX0833 standard Cat5e weatherproof coupler (higher cost alternative)](https://www.bulgin.com/us/products/front-panel-mount-connector-px0833-series-cat5e-shielded-coupler.html)
- [Hammond 1554 polycarbonate enclosure family](https://www.hammfg.com/part/1554T2GYCL)

This document is a **reversible design recommendation and concept CAD release**, not approval to drill or operate any electrical/pressure equipment.
