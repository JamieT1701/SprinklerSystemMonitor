"""Reproducible B1 first-order electrical budget. Assumptions != verified hardware."""
import json
from pathlib import Path
from math import sqrt

R_SENSE_OHM = 100.0
ADC_PGA_FULL_SCALE_V = 4.096
ADC_VDD_V = 3.3
ADC_LSB_V = ADC_PGA_FULL_SCALE_V / 32768
DIVIDER_TOP_OHM = 270000.0
DIVIDER_BOTTOM_OHM = 22000.0
DIVIDER_RATIO = DIVIDER_BOTTOM_OHM / (DIVIDER_TOP_OHM + DIVIDER_BOTTOM_OHM)

def make_receipt():
    currents = [0, 3.6, 4, 9.76, 12, 20, 20.5, 21, 26]
    samples=[]
    for i in currents:
        v=i/1000*R_SENSE_OHM
        samples.append({"current_mA":i,"sense_V":round(v,6),
                        "nominal_positive_adc_codes":round(v/ADC_LSB_V),
                        "shunt_power_mW":round((i/1000)**2*R_SENSE_OHM*1000,4)})
    divisions={str(v):round(v*DIVIDER_RATIO,5) for v in (0,18,24,30,36,40,44)}
    # Illustrative worst-case nominal loop-power point, not a certified PoE load.
    loop_w=24*0.026
    source_a=loop_w/(5.0*0.80)
    # Loop compliance at low supply, including illustrative limiter/cable losses.
    vtx=18-3-0.5-2
    return {
        "stage":"B1 bench candidate calculations only; no KiCad/ERC/DRC/hardware tests",
        "assumptions":{
            "pressure_span_psig":"provisional 0..150; contractor/sensor MPN required",
            "adc_vdd_V":ADC_VDD_V,
            "adc_analog_input_recommended_max_V":ADC_VDD_V,
            "ads1115_pga_full_scale_V":ADC_PGA_FULL_SCALE_V,
            "precision_shunt_Ohm":R_SENSE_OHM,
            "precision_shunt_tolerance":"target 0.1%, temperature coefficient <=25ppm/C; MPN TBD",
            "analog_divider_top_Ohm":DIVIDER_TOP_OHM,
            "analog_divider_bottom_Ohm":DIVIDER_BOTTOM_OHM,
            "terminal_divider":"nominal only; ADC loading, resistor tolerances, ESD/clamps excluded",
            "loop_supply_nominal_V":24,
            "low_loop_supply_test_V":18,
            "example_current_limit_mA":26,
            "five_volt_boost_efficiency_assumption":0.8,
            "limiter_drop_assumption_V":3,
            "cable_drop_assumption_V":0.5,
            "transmitter_minimum_voltage_assumption_V":8
        },
        "shunt_cases":samples,
        "divider_ratio":round(DIVIDER_RATIO,10),
        "divider_samples_V":divisions,
        "examples":{
            "pressure_54psig_0to150psig_loop_current_mA":round(4+16*(54/150),3),
            "pressure_54psig_adc_V":round((4+16*54/150)/1000*R_SENSE_OHM,4),
            "required_24V_loop_output_W_at_26mA":round(loop_w,4),
            "extra_5V_input_A_at_80pct_efficiency":round(source_a,4),
            "shunt_dissipation_W_at_26mA":round((0.026**2)*100,4),
            "transmitter_voltage_at_18V_supply_before_8V_need_V":round(vtx,2),
            "headroom_above_8V_transmitter_requirement_V":round(vtx-8,2)
        },
        "blockers":[
            "No measured 5V VSYS or PoE available-current envelope for a production module",
            "No validated 24V converter/power-path or safe indefinite field short-current limiter",
            "No input miswire/transient/ESD circuit verification for 24V direct on a field terminal",
            "No exact approved 4-20mA transmitter range/MPN/process port/temperature/proof pressure",
            "No analog ADC-loading/calibration/temperature error budget verified by bench",
            "No precise connector positions, creepage, board footprint or KiCad schematic/board"
        ],
        "sources":[
            "https://www.ti.com/product/ADS1115",
            "https://www.waveshare.com/wiki/ESP32-S3-ETH",
            "https://www.pololu.com/product/5588/specs",
            "https://infosys.beckhoff.com/content/1033/ioanalogmanual/3904850187.html"
        ]
    }

if __name__=="__main__":
    result=make_receipt()
    p=Path(__file__).with_name("calculation-receipt.json")
    p.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("Calculation receipt:",p)
    print("Loop at 26mA:",result["examples"]["required_24V_loop_output_W_at_26mA"],"W")
    print("ADC counts at 20mA:",next(s["nominal_positive_adc_codes"] for s in result["shunt_cases"] if s["current_mA"]==20))
