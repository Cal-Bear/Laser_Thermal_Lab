//DesignModeler JScript, version: Ansys DesignModeler 2021 R2 (Jun  1 2021, 09:34:08; 21,2021,151,1) SV4
//Created via: "Write Script: Sketch(es) of Active Plane"
// Written to: C:\Users\Jacky Li\Desktop\LTL\Ansys_learning\SYS.js
//         On: 10/16/21, 22:18:10
//Using:
//  agb ... pointer to batch interface


//Note:
// You may be able to re-use below JScript function via cut-and-paste;
// however, you may have to re-name the function identifier.
//

function planeSketchesOnly (p)
{

//Plane
p.Plane  = agb.GetActivePlane();
p.Origin = p.Plane.GetOrigin();
p.XAxis  = p.Plane.GetXAxis();
p.YAxis  = p.Plane.GetYAxis();

//Sketch
p.Sk1 = p.Plane.NewSketch();
p.Sk1.Name = "Sketch1";

//Edges
with (p.Sk1)
{
  p.Ln7 = Line(-11.64457017, 6.86366974, 15.33675096, 6.86366974);
  p.Ln8 = Line(15.33675096, 6.86366974, 15.33675096, -7.52636888);
  p.Ln9 = Line(15.33675096, -7.52636888, -11.64457017, -7.52636888);
  p.Ln10 = Line(-11.64457017, -7.52636888, -11.64457017, 6.86366974);
  p.Cr11 = Circle(1.78836258, 0.00000000, 4.04229178);
}

//Dimensions and/or constraints
with (p.Plane)
{
  //Constraints
  HorizontalCon(p.Ln7);
  HorizontalCon(p.Ln9);
  VerticalCon(p.Ln8);
  VerticalCon(p.Ln10);
  CoincidentCon(p.Ln7.End, 15.33675096, 6.86366974, 
                p.Ln8.Base, 15.33675096, 6.86366974);
  CoincidentCon(p.Ln8.End, 15.33675096, -7.52636888, 
                p.Ln9.Base, 15.33675096, -7.52636888);
  CoincidentCon(p.Ln9.End, -11.64457017, -7.52636888, 
                p.Ln10.Base, -11.64457017, -7.52636888);
  CoincidentCon(p.Ln10.End, -11.64457017, 6.86366974, 
                p.Ln7.Base, -11.64457017, 6.86366974);
  CoincidentCon(p.Cr11.Center, 1.78836258, 0.00000000, 
                p.XAxis, 1.78836258, 0.00000000);
}

p.Plane.EvalDimCons(); //Final evaluate of all dimensions and constraints in plane

return p;
} //End Plane JScript function: planeSketchesOnly

//Call Plane JScript function
var ps1 = planeSketchesOnly (new Object());

//Finish
agb.Regen(); //To insure model validity
//End DM JScript
