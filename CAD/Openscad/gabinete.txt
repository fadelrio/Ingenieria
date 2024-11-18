ANCHO = 4;
LARGO = 12;
ALTO = 4;
GROSOR_PARED = .3;
R_PARLANTES = 1.25;
ALTO_PATAS = 0.5;
GROSOR_MANIJA = 1;
ALTO_MANIJA = 1;

module cubo_redondeado( ancho, largo, alto, radio, centrado){
    minkowski(){
        cube([ancho - .1,largo - 2*radio, alto - 2*radio],centrado);
          rotate(90,[0,1,0])cylinder(.1, radio, center = true, $fn = 100);
    }
}

module cilindro_desplazado(radio, h, desplazamiento){
    translate([0,desplazamiento,0])
    rotate(90, [0,1,0])
    cylinder(h,r1= radio,r2= radio, center =true, $fn = 100);
}

module circulo_de_cilindros(r_cilindros, r_circunferencia, h, n_cilindros){
    for( i =[0: 360/n_cilindros :360]){
        rotate(i,[1,0,0])
        cilindro_desplazado(r_cilindros, h, r_circunferencia);
    }
}
module manija(){
    union (){
    color("#0000FF")
    translate([0,0,1+GROSOR_MANIJA/2])
    cube([LARGO/4, GROSOR_MANIJA,GROSOR_MANIJA], center = true); 
    for( i = [ 1:-2:-1]){
        translate([i*LARGO/8,0,0])
        difference(){
            rotate(90,[1,0,0])
            color("#0000FF")
            cylinder(GROSOR_MANIJA,r1 = ALTO_MANIJA+GROSOR_MANIJA,r2 = ALTO_MANIJA+GROSOR_MANIJA, center = true, $fn = 100);
            rotate(90,[1,0,0])
            
            cylinder(2,r1 = ALTO_MANIJA,r2 = ALTO_MANIJA, center = true, $fn = 100);
            translate([i*(-1),0,0])
            cube([2,2,(ALTO_MANIJA + GROSOR_MANIJA)*2],center =true);
            translate([i*(1),0,-1])
            cube([3,ALTO_MANIJA+GROSOR_MANIJA,ALTO_MANIJA+GROSOR_MANIJA],center =true);
        }
    }
}}


union(){  
    difference(){
        color("#FFC0CB")
        cubo_redondeado(ANCHO,LARGO,ALTO, 1, true);
        translate([-GROSOR_PARED,0,0])
        cubo_redondeado(ANCHO,LARGO - 2*GROSOR_PARED, ALTO -2*GROSOR_PARED,1,true);
        for (i =[-1:2:1]){
            translate([0,i*LARGO/4,0])
            for(j =[0:1:4]){
                circulo_de_cilindros(.1,R_PARLANTES-j*(R_PARLANTES/4),20,20-4*j);
            }
        }
        translate([-2,0,0])
        for(i=[-1:2:1]){
            for( j = [-1:2:1]){
                translate([0,i*5.555,j*1.555])
                rotate(90,[0,1,0])
                cylinder(2,r1=.05,r2=.05,center=true,$fn = 100);
            }
        }
        
    }
    for (i=[-1:2:1]){
        for(j=[-1:2:1]){
            color("#0000FF")
            translate([i*(ANCHO/2 - 0.75),j*(LARGO/2 -1.75), -ALTO/2 -ALTO_PATAS])
            cylinder(ALTO_PATAS,r1=0.10,r2=0.25,center=false,$fn = 100);
        }
    }
    translate([0,0,ALTO/2])
    rotate(90,[0,0,1])
    manija();
}
translate([-6,0,0])
difference(){
    color("#0000FF")
    cubo_redondeado(GROSOR_PARED,LARGO,ALTO,1,true);
    for(i=[-1:2:1]){
        for( j = [-1:2:1]){
            translate([0,i*5.555,j*1.555])
            rotate(90,[0,1,0])
            cylinder(2,r1=.05,r2=.05,center=true,$fn = 100);
        }
    }
}


        