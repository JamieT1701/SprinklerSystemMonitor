// Device Lab - enclosure project plate, revision P1 (2026-11-11)
// All dimensions in mm. This is a mechanical prototype, not a verified fit.
// Print AS EXPORTED: broad flat face down, four posts UP, no supports.
// Install inverted: posts against enclosure floor; screws enter from outside.
// The two perfboards and controller still need their own insulating PCB spacers.

part = "plate"; // "plate" or "post_test"
plate_w = 93;
plate_h = 146;
plate_t = 3;
corner_r = 5;
grid_pitch = 10;
grid_hole_d = 3.4;
grid_cols = 9;
grid_rows = 14;
post_inset = 10;
post_h = 6;              // clearance from enclosure floor to underside of plate
post_d = 10;
post_base_d = 14;
post_base_h = 1.5;       // tapered reinforcement at plate/post junction
pilot_d = 2.5;           // starting pilot for APPROX. 3mm plastic/self-tapping screw
pilot_depth = 7;         // blind; leaves 2mm of solid plate below the hole
pilot_leadin_h = 0.4;
pilot_leadin_d = 3.1;
max_screw_entry = 5;     // conservative allowed projection past case inner wall
hole_to_base_web = 1;    // minimum solid web between grid hole and base footprint
$fn = 64;

posts = [[post_inset,post_inset],
         [plate_w-post_inset,post_inset],
         [post_inset,plate_h-post_inset],
         [plate_w-post_inset,plate_h-post_inset]];
x0 = (plate_w-(grid_cols-1)*grid_pitch)/2;
y0 = (plate_h-(grid_rows-1)*grid_pitch)/2;

assert(pilot_depth < plate_t+post_h, "Pilot hole must remain blind");
assert(max_screw_entry < pilot_depth, "Screw must not bottom out");
assert(post_inset > post_base_d/2, "Post base must stay inside plate");
assert(post_d > pilot_d+4, "Insufficient boss wall thickness");

function near_post(x,y) = min([for(p=posts)
    sqrt(pow(x-p[0],2)+pow(y-p[1],2))]) <
    post_base_d/2 + grid_hole_d/2 + hole_to_base_web;

module plate_outline(w,h) {
    hull() for(x=[corner_r,w-corner_r]) for(y=[corner_r,h-corner_r])
        translate([x,y]) circle(r=corner_r);
}
module rounded_plate(w,h) {
    linear_extrude(height=plate_t) plate_outline(w,h);
}
module solid_post(x,y) {
    // Small overlaps keep the STL one connected, watertight body.
    translate([x,y,plate_t-0.01]) {
        cylinder(h=post_base_h+0.01, d1=post_base_d, d2=post_d);
        cylinder(h=post_h+0.01, d=post_d);
    }
}
module pilot(x,y) {
    ztop=plate_t+post_h;
    translate([x,y,ztop-pilot_depth]) cylinder(h=pilot_depth+0.02,d=pilot_d);
    translate([x,y,ztop-pilot_leadin_h])
        cylinder(h=pilot_leadin_h+0.02,d1=pilot_d,d2=pilot_leadin_d);
}
module project_plate() {
    difference() {
        union() {
            linear_extrude(height=plate_t) difference() {
                plate_outline(plate_w,plate_h);
                for(i=[0:grid_cols-1]) for(j=[0:grid_rows-1])
                    let(x=x0+i*grid_pitch,y=y0+j*grid_pitch)
                        if(!near_post(x,y)) translate([x,y]) circle(d=grid_hole_d);
            }
            for(p=posts) solid_post(p[0],p[1]);
        }
        for(p=posts) pilot(p[0],p[1]);
    }
}
module post_test() {
    difference() {
        union() {
            rounded_plate(20,20);
            solid_post(10,10);
        }
        pilot(10,10);
    }
}
if(part=="plate") project_plate();
else if(part=="post_test") post_test();
else assert(false,"Unknown part");
