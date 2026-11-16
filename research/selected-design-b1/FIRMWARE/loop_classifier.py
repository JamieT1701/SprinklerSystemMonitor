"""Bench-only B1 4-20 mA fault classification reference, not deployable firmware.

Model assumptions:
* 2-wire loop with measured shunt current, L+ terminal voltage and 24V loop rail.
* Process measurements use a 100-ohm shunt and independently powered ADC.
* Transmitter minimum voltage 8V is a *candidate*, NOT a universal rule.
* 0..150 psig is illustrative ONLY. The final range depends on the valve/site.
* No valve actuation, safety alarm, live PLC interface, or life-safety control.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from typing import Literal

Quality = Literal["VALID", "INVALID"]
State = Literal[
    "VALID", "ADC_FAULT", "LOOP_SUPPLY_FAULT", "LOOP_OPEN",
    "POSSIBLE_SHORT_TO_GROUND", "UNKNOWN_WIRING",
    "LOOP_COMPLIANCE_LOW", "SENSOR_FAULT_LOW", "UNDER_RANGE",
    "OVER_RANGE", "SENSOR_FAULT_HIGH"
]

@dataclass(frozen=True)
class Sample:
    current_ma: float
    terminal_lplus_v: float
    loop_supply_v: float
    adc_ok: bool = True
    reference_ok: bool = True

@dataclass(frozen=True)
class Settings:
    pressure_range_psig: float = 150.0  # NOT a field-approved sensor range
    min_loop_supply_v: float = 18.0
    max_loop_supply_v: float = 30.0
    transmitter_min_v: float = 8.0  # replace with actual selected MPN
    compliance_margin_v: float = 2.0
    shunt_ohm: float = 100.0
    open_circuit_current_ma: float = 0.5
    short_to_ground_lplus_v: float = 2.0
    open_terminal_ratio: float = 0.80

@dataclass(frozen=True)
class Result:
    quality: Quality
    state: State
    pressure_psig: float | None
    note: str

def invalid(state: State, note: str) -> Result:
    return Result("INVALID", state, None, note)

def classify(sample: Sample, cfg: Settings = Settings()) -> Result:
    """Classify a bench loop *sample*, never infer valve or fire-alarm status."""
    readings = (sample.current_ma, sample.terminal_lplus_v, sample.loop_supply_v)
    if not sample.adc_ok or not sample.reference_ok or not all(map(isfinite, readings)):
        return invalid("ADC_FAULT", "ADC, reference, or numeric data invalid")
    if (cfg.pressure_range_psig <= 0 or cfg.shunt_ohm <= 0
        or cfg.min_loop_supply_v >= cfg.max_loop_supply_v):
        raise ValueError("Invalid bench-only settings")
    if (sample.loop_supply_v < cfg.min_loop_supply_v
        or sample.loop_supply_v > cfg.max_loop_supply_v):
        return invalid("LOOP_SUPPLY_FAULT", "Excitation supply outside qualified band")
    if sample.current_ma < 0 or sample.terminal_lplus_v < 0:
        return invalid("UNKNOWN_WIRING", "Negative reading outside calibrated ADC interface")
    if sample.terminal_lplus_v > sample.loop_supply_v + 0.5:
        return invalid("UNKNOWN_WIRING", "External voltage / backfeed suspected")
    if sample.current_ma < cfg.open_circuit_current_ma:
        if sample.terminal_lplus_v >= cfg.open_terminal_ratio * sample.loop_supply_v:
            return invalid("LOOP_OPEN", "Open or unpowered transmitter (not proven severed)")
        if sample.terminal_lplus_v < cfg.short_to_ground_lplus_v:
            return invalid("POSSIBLE_SHORT_TO_GROUND", "L+ collapsed; confirm bench wiring")
        return invalid("UNKNOWN_WIRING", "Indeterminate low current and terminal voltage")
    # Do not classify 21+ mA as a cable short: transmitters may intentionally alarm high.
    return_v = cfg.shunt_ohm * sample.current_ma / 1000.0
    if sample.terminal_lplus_v - return_v < cfg.transmitter_min_v + cfg.compliance_margin_v:
        return invalid("LOOP_COMPLIANCE_LOW", "Transmitter differential voltage insufficient")
    if sample.current_ma < 3.6:
        return invalid("SENSOR_FAULT_LOW", "Loop under 3.6mA: possible transmitter fault")
    if sample.current_ma < 4.0:
        return invalid("UNDER_RANGE", "Near-zero under-range; not a certified valid pressure")
    if sample.current_ma <= 20.0:
        pressure = (sample.current_ma - 4.0) / 16.0 * cfg.pressure_range_psig
        return Result("VALID", "VALID", pressure, "Only measurement quality; not site NORMAL")
    if sample.current_ma < 21.0:
        return invalid("OVER_RANGE", "Over 20mA; unqualified out-of-range condition")
    return invalid("SENSOR_FAULT_HIGH", "Loop >=21mA; fault or miswire, not proof of a short")

def shunt_voltage_v(current_ma: float, shunt_ohm: float = 100.0) -> float:
    return current_ma / 1000.0 * shunt_ohm

def ideal_ads1115_counts(current_ma: float, shunt_ohm: float = 100.0) -> int:
    """Illustrative ADS1115 +/-4.096 V PGA, 0.125mV/LSB, positive range."""
    volts = shunt_voltage_v(current_ma, shunt_ohm)
    if volts < 0 or volts > 3.3:
        raise ValueError("Outside nominated 3.3V ADC pin operating range")
    return round(volts / 0.000125)
