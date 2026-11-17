"""B1 supplier-specific bench profile and transparent loop budgets.

These are *manufacturer-derived candidates*, not verified component fits,
actual calibration, installed site thresholds or approved fault safety.
"""
from dataclasses import dataclass
from math import isfinite
from loop_classifier import Settings, Sample, Result, classify

@dataclass(frozen=True)
class SensorProfile:
    mpn: str
    full_scale_psig: float
    min_sensor_supply_v: float
    max_sensor_supply_v: float
    accuracy_full_scale_percent: float
    nominal_min_ma: float
    nominal_max_ma: float
    documented_under_range_ma: float
    documented_over_range_ma: float
    supply_contact: int
    current_return_contact: int
    unused_contacts: tuple[int, ...]
    manufacturer_pdf: str

SPTD25_0100 = SensorProfile(
    mpn="SPTD25-20-0100H",
    full_scale_psig=100.0,
    min_sensor_supply_v=8.5,
    max_sensor_supply_v=36.0,
    accuracy_full_scale_percent=0.5,
    nominal_min_ma=4.0,
    nominal_max_ma=20.0,
    documented_under_range_ma=3.0,
    documented_over_range_ma=25.0,
    supply_contact=1,
    current_return_contact=2,
    unused_contacts=(3,4),
    manufacturer_pdf="https://cdn.automationdirect.com/static/specs/prosensesptd25transmitters.pdf"
)

# Different manufacturer connector pinout. A *separate* hardware/harness profile
# is needed to qualify LPPT, despite the same A-coded M12 physical connector.
LPPT25_PINOUT = {
    "mpn": "LPPT25-20-0100H",
    "supply_contact": 1,
    "ground_contact": 2,
    "current_return_contact_choices": (3,4),
    "manufacturer_pdf": "https://cdn.automationdirect.com/static/specs/achievelpptprestrans.pdf"
}

def sptd25_bench_settings() -> Settings:
    """Manufacturer-specific behavior, NOT an approved site pressure alarm."""
    return Settings(pressure_range_psig=100.0,
                    transmitter_min_v=8.5,
                    sensor_profile="SPTD25-20-0100H")

def classify_sptd25(sample: Sample) -> Result:
    return classify(sample, sptd25_bench_settings())

def minimum_required_loop_source_v(
    sensor_min_v: float=8.5, current_ma: float=21.5,
    shunt_ohm: float=100.0, extra_series_ohm: float=0.0,
    voltage_drop_budget_v: float=0.0
) -> float:
    """Conservative voltage requirement, excluding unspecified converter behavior.

    The current is user supplied; for SPTD manufacturer's load formula use 21.5mA.
    """
    nums=(sensor_min_v,current_ma,shunt_ohm,extra_series_ohm,voltage_drop_budget_v)
    if not all(isfinite(n) for n in nums) or min(nums)<0:
        raise ValueError("Invalid loop budget parameter")
    return sensor_min_v + (current_ma/1000)*(shunt_ohm+extra_series_ohm)+voltage_drop_budget_v

def nominal_efuse_limit_ma(r_ilim_kohm: float) -> float:
    """TI TPS2662 datasheet IOL=6.636/RILIM [A, kOhm], *not rated min/max trip*."""
    if not isfinite(r_ilim_kohm) or r_ilim_kohm <=0:
        raise ValueError("Invalid ILIM resistor")
    return (6.636/r_ilim_kohm)*1000

def pressure_from_nominal_current(current_ma: float,
                                  profile: SensorProfile=SPTD25_0100) -> float:
    if not isfinite(current_ma) or not profile.nominal_min_ma<=current_ma<=profile.nominal_max_ma:
        raise ValueError("No calibrated pressure outside sensor's 4-20mA span")
    return profile.full_scale_psig*(current_ma-profile.nominal_min_ma)/(profile.nominal_max_ma-profile.nominal_min_ma)

def nominal_transmitter_uncertainty_psig(profile: SensorProfile=SPTD25_0100) -> float:
    """Sensor-only full-scale error at manufacturer's specified conditions.

    System uncertainty also includes calibration, temperature, drift,
    shunt, ADC, wiring, installation and pressure-domain effects.
    """
    return profile.full_scale_psig*profile.accuracy_full_scale_percent/100
