#Pressure Drop Calculator
#Carlos J. Sola

from math import log

def darcy_weisbach(f_d_w,L,D,V,g):
#This function calculates the the major pressure drop across a pipe
#using the darcy weisbach method
#h_f = Darcy_Weisbach head loss (meters)
#f_d_w = Darcy-Weisbach friction factor (unitless)
#L = length of pipe (meters)
#D = pipe diameter (meters)
#V = velocity (meters/second)
#g = gravitational constant (meters/seconds^2)
	
	h_f_major = f_d_w * (L/D) * (pow(V,2)/(2*g))
	
	return h_f_major
	
def reynolds_number(V,D,v):
#This function calculates the Reynolds number
#V = velocity (meters/second)
#D = pipe diameter (meters)
#v = kinematic viscosity (meters^2 / sec)

	reynolds = V*D/v
	
	return reynolds

def churchill_friction_factor(Re,k,D):
#This function calculates the friction factor to be used in the darcy_weisbach function
#the method used here is the Chruchill method since it covers both the laminar and turbulent ranges
#Re = Reynolds number
#k = absolute roughness (meters), this page has some pretty usefull values:
	# http://www.engineeringtoolbox.com/major-loss-ducts-tubes-d_459.html
#D = pipe diameter (meters)
#f = Churchill friction factor


	A= pow(2.457*log(1/(pow(7/Re,0.9)+(0.27*k/D))),16)
	B =pow(37530/Re,16)
	f = 8 * pow(pow(8/Re,12) + 1 /(pow(A+B,1.5)),1/12)
	return f

def minor_losses(V,g,f,deg):
#This function calculates the pressure drop due to bends
#V = velocity (meters/second)
#g = gravitational constant (meters/seconds^2)
#f = Churchill friction factor
#deg = bend degrees ( in degrees, not radians!)
	k_factor = 0.138888889* pow(deg,3) + 0.130952381*pow(deg,2) + 0.7063492063*deg + 1
	K = k_factor * f
	h_f_minor = K * pow(V,2) / (2 * g)
	return h_f_minor

def input_minor_loss_angles():
	angles = []
	print "Input the bend angles in degrees. Type \"done\" when finished."
	finished = "no"
	while finished is "no":
		val_input = raw_input("Enter angle (deg),\"done\" when finished: ")
		if val_input != "done":
			try:
				flt_val_input = float(val_input)
			except ValueError:
				print "Input invalid.Please try again!"
			else:
				angles.append(flt_val_input)
		else:
			print "Finished inputing angles."
			finished = "yes"

	return angles

def sum_minor_losses(V,g,f,angles):
	total = 0.0
	for i in range(0,len(angles)):
		total = total + minor_losses(V,g,f,angles[i])
	return total

def total_losses(V,g,D,v,k,L,bend_angles):
	total_drop = darcy_weisbach(churchill_friction_factor(reynolds_number(V,D,v),k,D),L,D,V,g) + sum_minor_losses(V,g,churchill_friction_factor(reynolds_number(V,D,v),k,D),bend_angles)
	return total_drop

def main():
	print "\n Pressure Drop Calculator\n"
	print "This program calculates the pressure drop across a pipe due to friction loss"
	print "and bends.\n"
	print "Method: Darcy Weisbach using a Churchill friction factor."
	print "As described in Analysis and Design of Energy Systems, 3rd Edition"
	print "B.K. Hodge, Robert O. Taylor.\n"
	
	print "You will be prompted to input the following: "
	print "Flow Velocity (m/s), Pipe length (m), Pipe diameter (m),bends (deg)"
	print "Kinematic viscosity (m^2/s) and Pipe Absolute Roughness (m)\n"
	
	V = input("Please input flow velocity (m/s): ")
	L = input("Please input pipe length (m): ")
	D = input("Please input pipe diameter (m): ")
	v = input("Please input the Kinematic viscosity (m^2/s): ")
	k = input("Please input pipe absolute roughness (m): ")
	g = 9.81
	
	bends = input_minor_loss_angles()
	
	print "Calculating pressure drop..."
	result = total_losses(V,g,D,v,k,L,bends)
	print "Head Loss: " + str(result) + " meters"
	raw_input()

if __name__ == "__main__":
    main()


	


