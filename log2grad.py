#input logfile
import numpy as np
import tabulate


logInput = open("stena-U.log","r")
# elemType, iteration, element, nGaussPoint, GaussPoint_x, GaussPoint_y, F_i ...

#outputfile
Fout = open("Fout.txt", "w")
n = 4
output = []
#settings
elemType = "PHANTOM"


line = ""
array1 = []
for i in logInput: 
    line = i.replace("\n","")
    if elemType in line:
        #print(line)
        array1.append(line)

array_rev = array1[::-1]

last_line = array_rev[0].split(";")
iters = int(last_line[1])
nElem = int(last_line[2]) # kaj ce je vec elementov?
nGaussPoint = int(last_line[3])

print("Iterations : ", iters, "Number of elements : ", nElem, "Integration points : " ,nGaussPoint)

reversed_array_sorted = []
for i in range(0, len(array_rev)):
    line = array_rev[i].split(";")
    line.pop(0)
    line = [float(j) for j in line ]
    reversed_array_sorted.append(line)

for k in range(0, len(reversed_array_sorted)):
    line = reversed_array_sorted[k]
    n = int(nGaussPoint * nElem)
    if int(line[0]) == iters:# and iters > 0: # iters > 0 -> ni zacetne iteracije 0
        for i in range(0, n):
            output.append(reversed_array_sorted[k+i])
        k += n
        iters -= 1


# back to original order:
output = output[::-1]
line_out = ""
output_np = []
for i in output:
    for k in range(0, len(i)):
        if k < 3:
            line_out += str(int(i[k])) + "\t"
        elif k < len(i):
            line_out += str(float(i[k])) + "\t"
        else:
            line_out += str(float(i[k]))
            break
    
    Fout.write(line_out)
    output_np.append(i)
    Fout.write("\n")
    line_out = ""
#Ustvati Fout, ki bo uporablen za gradient.txt !

inp = open("stena-U.inp", "r")
x_0 = 0.0
x_end = 0.0
step = 0.0
boundary = ""
for j,i in enumerate(inp):
    if "*Step, name=loading, nlgeom=YES" in i:
        if "*Static" in inp.readline(j+1):
            boundary = inp.readline(j+2).split(",")
            x_0 = float(boundary[0])
            x_end = float(boundary[1])
            step = float(boundary[-1])

x = np.array(np.arange(0, x_end+step, step ))
output_np = np.array(output_np)


GP = 1 # gaussova tocka ki nas zanima 

#print(output_np[1,3])
#remove 1-5 column

for i in range(0,5):
    print(output_np.shape[1])
    output_np = np.delete(output_np,0 ,1)



#print(output_np)

#print(output_np.shape[0])
F = []
for i in range(0+GP-1,output_np.shape[0],nGaussPoint ):
    F.append( output_np[i])
    #print(i, output_np[i])

F = np.array(F)
#F = F.flatten()
print(tabulate.tabulate(F))


if x.shape[0] != F.shape[0]:
    print("Size Error")

#for i in range(0, int(x.shape[0])):
    #f = F
    #print(F.flatten())

O = np.column_stack((x, F))
O[0,1] = 0
O[0,2] = 0
O[0,3] = 0
O[0,4] = 0
O[0,5] = 0

np.savetxt("Gradient_abaqus.txt",O)
#print(tabulate.tabulate(O))
