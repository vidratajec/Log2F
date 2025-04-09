import json
import numpy as np

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.9f') # da ne spremeni majhnih stevil na 0

#settings:
elemType = "PHANTOM" # ime tipa elementa ki nas zanima
save2TXT = False
save2JSON = True

input_file = "stena-4U_starman.log"
output_file = "Grad_"+ elemType +".json"

input_log = open(input_file, "r")

# korak 1 in 2:
line = ""
data = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]) # for vstack
after_iter0 = False

output = {}

for i in input_log:
    if elemType in i:
        line = i.replace("\n", "") #s odstrani newline
        line = line.split(";")
        iter, elem, n_GP = int(line[1]), int(line[2]), int(line[3]) # iteracije, element, st. gaussove integracijse tocke
        GP_x, GP_y = float(line[4]), float(line[5]) # x,y koordinati n_GP-te int.g. tocke
        f1, f2, f3, f4, f5 = float(line[6]), float(line[7]), float(line[8]), float(line[9]), float(line[10])
        #print(line)
        #print(iter,elem,n_GP,GP_x, GP_y,f1, f2, f3, f4, f5)
        
        if iter == 0 :
            after_iter0 = True
        
        if (after_iter0 == True and iter > 0 ):
            data = np.vstack((data, [iter,elem,n_GP,GP_x, GP_y,f1, f2, f3, f4, f5]))
            print(iter,elem,n_GP,GP_x, GP_y,f1, f2, f3, f4, f5)

            #data entry
            entry = {
                "x" : GP_x,
                "y" : GP_y,
                "F" : [f1, f2, f3, f4, f5]
            }

            output.setdefault(iter, {}).setdefault(elem, {})[n_GP] = entry

if save2TXT:        
    np.savetxt("data2.txt",data)

if save2JSON:
    out = open(output_file, "w");
    json.dump(output,out, indent=2)
