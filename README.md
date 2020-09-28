# fathom_plotting
Program that takes outputs from fathom and plots them in a pretty seaborn graph.

This program assumes the inputs EXACTLY as thy are listed in the headers of 
Fathom Output.xlsx. 

If some values are not known, just leave the column blank. E.G you may not know/want
the AOR/POR Values. 

Each Sheet should contain different pump speeds - as many as you want

DO NOT change the sheet names."Sheet1", "Sheet2" etc strings are used for looping within the program.

NPSHa is calulated for 100% flow only. Minor velocity losses are not accounted for. 

Efficiancy is not currently graphed as it gets very messy. 
Only Flows in L/s and lengths in metres are supported. Please convert to these prior to using the program. 

Headers are as follows:

Speed (%)	| Pump Flow	| Pump Head |	System Curve Flow	| System Curve Head |	Efficiancy Flow	| Efficiancy Percent |
AOR Flow |	AOR Head | POR Flow |	POR Head |	Inlet Resevoir Level |	NPSH Elevation Reference |
Suction Pipe Diameter	|	Pipe Friction Factor	|	Suction Pipe Length | NPSHR Flow	|	NPSHR Head


Speed (%) - Percent  - Speed for chosen curve details. 

Pump Flow -  L/s - Pump flows from Fathom graph

Pump Head - m - Pump Head from Fathom Graph

System Curve Flow - L/s - System Flow from Fathom Graph

System Curve Head - m - System Head from Fathom Graph

Efficiancy Flow - L/s - Efficiancy flow from pump supplier.  

Efficiancy Percent- Percent - Efficiancy percent from pump supplier.  

AOR Flow - L/s - Allowable Operating Pressure flows, max and min flows - any order

AOR Head - m - Allowable Operating Pressure Heads, max and min - same as flow order

POR Flow - L/s - Preferred Operating Pressure flows, max and min flows - any order

POR Head - m - Preferred Operating Pressure Heads, max and min - same as flow order

Inlet Resevoir Level - m - Inlet resevoir level from Fathom. Can be negative (usually is). Used to caluclated NPSHa

NPSH Elevation Reference - m - Pump Inlet Centerline level from Fathom, OR NPSHa reference point, if different than the 
centerline level. Can be negative (usually is). Used to caluclated NPSHa.

Suction Pipe Diameter - m - Suction pipe diameter. Currently only a single diameter is supported. Used to calulate NPSHa

Pipe Friction Factor - Dimensionless - Moody friction factor. This is usually obtained by a profile graph for the suction
pipework and choosing "friction factor". Used to caluclated NPSHa

Suction Pipe Length - m - Suction pipework length. Used to caluclated NPSHa

NPSHr flow - L/s - NPSHr flow from the pump supplier. 

NPSHR Head - m - NPSHR Head from the pump supplier. 

The graphs typically work, I've tried to ensure any offsets are functions of the x/y-axis values rather than hard coded, however details around the placement of legend and text may require tweaking. 
