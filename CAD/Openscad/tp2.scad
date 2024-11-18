
radio_array = 1.25;
radio_cilindro = .25;
n_cilindros = 10;

module cilindro(){
    translate([radio_array,0,0])
    rotate(-90,[1,0,0])
        cylinder(h=10, r=radio_cilindro, $fn=50);
}
module cubo_redondeado(x,y,z,r,c){
    cube([(x-r), (y-r), (z-1)], c);
    minkowski(){
        cube([(x-2*r), (y-1), (z-2*r)], c);
        rotate(-90,[1,0,0])
        cylinder(1,r,center = true, $fn = 50);
        
    }
}


difference(){
    cubo_redondeado(12,4,4,1,true);
    translate([0,-1,0])
        cubo_redondeado(11.5,5,3.5,1,true);
    for(i=[-1:2:2]){
        translate([3*i,0,0])
            for (i=[0 : 360/n_cilindros : 360]){
                rotate(i,[0,1,0])
                cilindro();
            }
        }
}
