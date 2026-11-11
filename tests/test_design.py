"""Design-only electrical consistency checks. Not a physical or safety certification."""
import json, math, unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT/'hardware/two-terminal-design.json').read_text())
HTML = (ROOT/'docs/index.html').read_text()
class Inputs(HTMLParser):
    def __init__(self):
        super().__init__(); self.steps=[];self.wires=[]
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=='input':
            if 'data-step' in a:self.steps.append(a['data-step'])
            if 'data-wire' in a:self.wires.append(a['data-wire'])
def solve_network(sig=None,test_supply=None):
    # Independent nodal DC solution: ideal high-impedance ADC; capacitor branches open.
    resist=[('SIG','DIV',10000),('DIV','MID',10000),('MID','GND',4700),('DIV','A0',1000)]
    fixed={'GND':0.0}
    if sig is not None:fixed['SIG']=sig
    else:
        fixed['SIM']=test_supply;resist.append(('SIM','SIG',10000))
    unknown=[n for n in ['SIG','DIV','MID','A0'] if n not in fixed]
    a=[[0.0]*(len(unknown)+1) for n in unknown]
    for x,y,r in resist:
        for n,o in [(x,y),(y,x)]:
            if n not in unknown:continue
            i=unknown.index(n);a[i][i]+=1/r
            if o in unknown:a[i][unknown.index(o)]-=1/r
            else:a[i][-1]+=fixed[o]/r
    for i in range(len(a)):
        j=max(range(i,len(a)),key=lambda j:abs(a[j][i]));a[i],a[j]=a[j],a[i]
        pivot=a[i][i];a[i]=[x/pivot for x in a[i]]
        for j in range(len(a)):
            if j!=i:
                factor=a[j][i];a[j]=[x-factor*y for x,y in zip(a[j],a[i])]
    return {**fixed,**dict(zip(unknown,[row[-1] for row in a]))}
class DesignTests(unittest.TestCase):
    def test_exact_three_external_connections(self):self.assertEqual(len(D['field_connections']),3)
    def test_exact_two_blocks_three_positions(self):
        t=[x for x in D['field_connections'] if x['type']=='terminal_block']
        self.assertEqual([x['id'] for x in t],['J1','J2']);self.assertEqual([x['positions'] for x in t],[3,3])
    def test_both_blocks_board_b(self):
        self.assertTrue(all(x['board']=='B' for x in D['field_connections'] if x['type']=='terminal_block'))
    def test_two_small_boards(self):self.assertEqual([v['size_mm'] for v in D['boards'].values()],[[70,50],[70,50]])
    def test_no_pin_assigned_twice(self):
        pins=[p for ps in D['nets'].values() for p in ps];self.assertEqual(len(pins),len(set(pins)))
    def test_terminal_assignments(self):
        lookup={p:n for n,ps in D['nets'].items() for p in ps}
        for c in D['field_connections']:
            for p,n in c.get('pins',{}).items():self.assertEqual(lookup[c['id']+'.'+p],n)
    def test_no_sensor_plus5_on_adc(self):self.assertNotIn('ADS.VDD',D['nets']['+5V']);self.assertIn('ADS.VDD',D['nets']['+3V3'])
    def test_temp_data_is_gpio18_not_adc(self):
        self.assertIn('ESP.GPIO18',D['nets']['TEMP_DATA']);self.assertIn('J2.2',D['nets']['TEMP_DATA']);self.assertFalse(any(x.startswith('ADS.') for x in D['nets']['TEMP_DATA']))
    def test_pullup_exactly_one_47k(self):
        pulls=[r for r in D['resistors'].values() if 'TEMP_DATA' in r['nodes']]
        self.assertEqual(len(pulls),1);self.assertEqual(pulls[0]['ohms'],4700);self.assertEqual(set(pulls[0]['nodes']),{'+3V3','TEMP_DATA'})
    def test_pressure_has_no_direct_wire_bypass(self):self.assertNotIn('ADS.A0',D['nets']['PRESS_SIG']);self.assertIn('ADS.A0',D['nets']['A0'])
    def test_component_leads_match_netlist(self):
        for part in ['resistors','capacitors']:
            for ref,c in D[part].items():
                for i,n in enumerate(c['nodes'],1):self.assertIn(ref+'.'+str(i),D['nets'][n])
    def test_supply_bypass_is_not_data_capacitor(self):
        self.assertEqual(set(D['capacitors']['C2']['nodes']),{'+3V3','GND'})
        self.assertFalse(any('TEMP_DATA' in c['nodes'] for c in D['capacitors'].values()))
    def test_five_installed_resistors_two_47k(self):
        self.assertEqual(len(D['resistors']),5);self.assertEqual(sum(r['ohms']==4700 for r in D['resistors'].values()),2)
    def test_all_ground_returns_in_one_net(self):
        self.assertTrue(set(['J1.2','J2.3','ADS.GND','ESP.GND','R3.2']).issubset(D['nets']['GND']))
    def test_gpio_assignments_and_address(self):
        self.assertEqual(D['nets']['SDA'],['ESP.GPIO17','ADS.SDA']);self.assertEqual(D['nets']['SCL'],['ESP.GPIO16','ADS.SCL']);self.assertIn('ADS.ADDR',D['nets']['GND'])
    def test_nine_interassembly_wires(self):self.assertEqual([w['id'] for w in D['harness']],['W%02d'%i for i in range(1,10)])
    def test_ratio(self):self.assertAlmostEqual(D['assumptions']['divider_ratio'],14700/24700,12)
    def test_pressure_0_50_150(self):
        for psi in [0,50,150]:
            sig=.5+psi/150*4;v=solve_network(sig=sig)['A0'];self.assertAlmostEqual((v/(14700/24700)-.5)*37.5,psi,9);self.assertTrue(0<=v<3.3)
    def test_bench_simulator_independent_network(self):
        v=solve_network(test_supply=3.3)['A0'];self.assertAlmostEqual(v,1.3979827089337176,10);self.assertAlmostEqual((v/(14700/24700)-.5)*37.5,69.33717579250721,8)
    def test_undriven_sensor_not_zero_psi(self):
        self.assertGreater(solve_network(sig=.5)['A0'],.29);self.assertAlmostEqual(solve_network(sig=0)['A0'],0)
    def test_ads_config_decode(self):
        c=0xC383;self.assertEqual((c>>12)&7,4);self.assertEqual((c>>9)&7,1);self.assertEqual((c>>8)&1,1);self.assertEqual((c>>5)&7,4);self.assertEqual(c&3,3)
    def test_web_checklists(self):
        p=Inputs();p.feed(HTML);self.assertEqual(p.steps,[str(i) for i in range(1,13)]);self.assertEqual(p.wires,['W%02d'%i for i in range(1,10)])
    def test_no_remote_images_or_operational_claim(self):
        self.assertNotIn('<img',HTML);self.assertIn('NOT been deployed',HTML);self.assertIn('not live monitoring',HTML)
    def test_no_private_network_or_credentials(self):
        for s in ['192.168.','SPRINKLER_OTA_PASSWORD','ota-password.txt','sk-proj-']:
            self.assertNotIn(s,HTML)
if __name__=='__main__':unittest.main(verbosity=2)
