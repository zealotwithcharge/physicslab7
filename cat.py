import math
import argparse
import sympy
import matplotlib.pyplot as plt



distances = [2.659,1.659,.9525,.575]
angle1s = [60,65,85,101]
h = 0.125
r = 0.2775
pi = math.pi
m = 0.0164
t = []
v = []
ew = []
table =[[],[],[],[]]
for i in range(4):
    d = distances[i]
    a1 = angle1s[i]*2*math.pi/360
    a2 = (90-float(angle1s[i]))*2*math.pi/360

    
    x = sympy.symbols('x')
    equation = sympy.Eq((d+r*math.cos(a1))/(math.cos(a2)*x)-((0.5*9.8*x**2-h-r*math.sin(a1))/(math.sin(a2)*x)),0)
    t1 = list(sympy.solveset(equation,x))




    if t1[0] > 0:
        t.append(t1[0])
    else:
        t.append(t1[1])

    v.append((d+r*math.cos(a1))/(math.cos(a2)*t[i]))
    ew.append(v[i]**2*m*0.5)
    table[i].append(str(distances[i])+' m')
    table[i].append(str(angle1s[i])+' degrees')
    table[i].append('{:.3f}'.format(t[i])+' s')
    table[i].append('{:.3f}'.format(v[i])+' m/s')
    table[i].append('{:.3f}'.format(ew[i])+' N')
print(t)
print(v)
print(ew)
r1 = 0.15
ss = [(i+1)*10*2*math.pi/360*r1 for i in range(18)]
ia1s = [180, 163, 144, 125]
ir1s = [angle*2*math.pi/360 for angle in ia1s]


# solve for a and b
def best_fit(X, Y):

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    return a, b

fig, ax = plt.subplots()  

forces = [0.217, 0.175,0.259,0.284,0.259,0.350,0.400,0.400,0.539,0.509,0.617,0.692,0.761,0.784,0.884,0.802,0.809,0.975]
a, b = best_fit(ss, forces)

iw1s = [0.5*(a+b*(angle*r1))*(angle*r1) for angle in ir1s]
for i,w in enumerate(iw1s):
    table[i].append('{:.3f}'.format(w)+' N')

yfit = [a + b * xi for xi in ss]

plt.figure(1) 

color = []
for tab in table:
    colour = []
    for item in tab:
        colour.append('w')
    color.append(colour)
notches = ['Notch #1','Notch #2','Notch #3','Notch #4']
columns = ['Distance','Launch Angle of Arm','Estimated Time Travelled','Estimated Initial Velocity','Estimated Work \n by 1/2*m*v^2','Estimated Work by \nintegral(Force * ds)']
ax.set_axis_off()
table1 = ax.table(table,color,'right',rowLabels =notches,colLabels=columns,loc = 'center')
table1.set_fontsize(36)
table1.scale(2,2)


plt.figure(2)
plt.scatter(ss,forces)

plt.xlabel('s (m)')
plt.ylabel('Force (N)')
plt.title('Force vs s ')

plt.tight_layout()
plt.plot(ss,yfit)
plt.text(0.7, 0.5,f'{a:.2f}+{b:.2f}*x', horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes)

plt.figure(3)
plt.scatter(iw1s,v)
for i,w in enumerate(iw1s):
    plt.annotate('({:.3f},{:.3f})'.format(w,v[i]),(w,v[i]))
plt.xlabel('Work (N*m)')
plt.ylabel('Initial Velocity (m/s)')
plt.title('Work vs Initial Velocity')

plt.show()
