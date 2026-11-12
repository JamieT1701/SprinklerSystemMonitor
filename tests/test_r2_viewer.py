"""Static/reproducibility checks for the iPhone-friendly R2 3D browser viewer.
Browser interactions independently checked in headless Chrome CDP on Oscar.
"""
import json,pathlib,re,struct,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
PAGE=ROOT/"docs/r2-viewer.html"
LAYOUT=ROOT/"cad/fusion/DeviceLabR2Detail/assembly-layout.json"
TOP=ROOT/"docs/assets/fusion-r2-layout-top.png"
ISO=ROOT/"docs/assets/fusion-r2-assembly-isometric.png"
MOBILE=ROOT/"docs/assets/r2-viewer-iphone-viewport-qa.png"

class TestViewer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=PAGE.read_text(encoding="utf8")
        m=re.search(r'<script type="application/json" id="modelData">(.*?)</script>',cls.html,re.S)
        if not m:raise AssertionError("Embedded model JSON not found")
        cls.embedded=json.loads(m.group(1))
        cls.original=json.loads(LAYOUT.read_text(encoding="utf8"))
    def test_embedded_browser_model_matches_repo_source(self):
        self.assertEqual(self.embedded,self.original)
    def test_no_cdn_external_dependency_or_secret_data(self):
        self.assertNotIn("script src=",self.html.lower())
        self.assertNotIn("http://",self.html.lower())
        self.assertNotIn("https://",self.html.lower())
        self.assertNotIn("api_key",self.html.lower())
        self.assertIn('name="viewport"',self.html)
        self.assertIn('touch-action:none',self.html)
    def test_views_and_controls_wired(self):
        for needle in ['data-view="iso"','data-view="top"','data-view="side"',
                       'id="explode"','id="lid"','id="case"','id="mounts"',
                       'id="save"','pointermove','pointercancel','toDataURL("image/png")']:
            self.assertIn(needle,self.html)
    def test_render_and_iphone_evidence_png_dimensions(self):
        expect={TOP:(1800,2250),ISO:(2200,1560),MOBILE:(1170,2532)}
        for f,(w,h) in expect.items():
            b=f.read_bytes()
            self.assertGreater(len(b),12000)
            self.assertEqual(b[:8],b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack_from(">II",b,16),(w,h))
    def test_technical_and_safety_disclosures(self):
        for needle in ["NOT A PRINT OR DRILL TEMPLATE","separate 3-screw blocks",
                       "original mesh is preserved separately","supplemental sprinkler monitoring"]:
            # Text occurs in UI or in source-derived JS (case insensitive).
            self.assertIn(needle.lower(),self.html.lower())
    def test_sized_board_envelopes_remain_70_50_and_72_8_21(self):
        box={b["id"]:b["xy"] for b in self.embedded["boards"]}
        for name,width,height in [("A",70,50),("B",70,50),("ESP",72.8,21)]:
            x0,y0,x1,y1=box[name]
            self.assertAlmostEqual(x1-x0,width)
            self.assertAlmostEqual(y1-y0,height)

if __name__=="__main__":
    unittest.main()
