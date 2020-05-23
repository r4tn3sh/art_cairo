#!/usr/bin/python3
import math
import cairo
import random

random.seed(2)
noofcenters = 4
#Canvas size
WIDTH, HEIGHT = 1024, 1024

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
ctx.set_line_width(0.01)

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def draw_spiral(edge_x, edge_y, rot, M, delta, deltainc, N):
    #print(M)
    #print(edge_x[0], edge_y[0])
    ctx.move_to(edge_x[0], edge_y[0])
    for loop in range(0,N):
        if rot==0: #clockwise rotation
            idx = (loop)%M
            nxt_x = edge_x[(idx+1)%M]*(1-delta) + edge_x[(idx+2)%M]*delta
            nxt_y = edge_y[(idx+1)%M]*(1-delta) + edge_y[(idx+2)%M]*delta
            edge_x[(idx+1)%M] = nxt_x
            edge_y[(idx+1)%M] = nxt_y
        else: #anticlockwise rotation
            idx = (M-(loop)%M)%M
            nxt_x = edge_x[(idx+M-1)%M]*(1-delta) + edge_x[(idx+M-2)%M]*delta
            nxt_y = edge_y[(idx+M-1)%M]*(1-delta) + edge_y[(idx+M-2)%M]*delta
            edge_x[(idx+M-1)%M] = nxt_x
            edge_y[(idx+M-1)%M] = nxt_y
        ctx.line_to(nxt_x, nxt_y)
        delta = min((1+deltainc)*delta, 0.5)

# Equation of perpendicular bisector
def get_prpd_eq(x1, y1, x2, y2):
    m = -(x2-x1)/(y2-y1)
    b = ((y1+y2)/2) - m*((x1+x2)/2)
    return m, b

def veclen(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

min_x = 0.1
max_x = 0.9
delta_base = 0.05
edge_x = [0]*5 #assuming 4 edges
edge_y = [0]*5

# Get 4 random coordinates for 4 edges
a1 = random.uniform(min_x, max_x)
a2 = random.uniform(min_x, max_x)
a3 = random.uniform(min_x, max_x)
a4 = random.uniform(min_x, max_x)

base_x = [0]*noofcenters
base_y = [0]*noofcenters
#m = [[0]*(noofcenters)]*noofcenters
#b = [[0]*(noofcenters)]*noofcenters
m = [[0 for x in range(noofcenters)] for y in range(noofcenters)]
b = [[0 for x in range(noofcenters)] for y in range(noofcenters)]
ax = [[0 for x in range(noofcenters+5)] for y in range(noofcenters)]
ay = [[0 for x in range(noofcenters+5)] for y in range(noofcenters)]
angle_t = [[0 for x in range(noofcenters+5)] for y in range(noofcenters)]
#ax = [0]*(noofcenters)
#ay = [0]*(noofcenters)
Nidx = [0]*noofcenters
# Choose random vornoi center points
for loop in range(0,noofcenters):
    base_x[loop] = random.uniform(min_x, max_x)
    base_y[loop] = random.uniform(min_x, max_x)
    ctx.move_to(base_x[loop], base_y[loop])
    ctx.arc(base_x[loop],base_y[loop],0.005, 0, 2*(math.pi))
    ctx.fill

#print("---------------")
# Save perpendicular bisectos
idx = 0
for loop1 in range(0,noofcenters):
    for loop2 in range(loop1+1, noofcenters):
        m[loop1][loop2], b[loop1][loop2] = get_prpd_eq(base_x[loop1], base_y[loop1], base_x[loop2], base_y[loop2])
        m[loop2][loop1] = m[loop1][loop2]
        b[loop2][loop1] = b[loop1][loop2]
        #print("@@@@",loop1," ",loop2," ",m[loop1][loop2]," ",b[loop1][loop2])

        continue

        #following is only for visual debugging
        move_flag = 0
        for loop3 in range(0, 4):
            tidx = 3
            if not ((loop1==tidx and loop2!=tidx) or (loop2==tidx and loop1!=tidx)):
                continue
            if loop3==0: #y=0
                tvar = -b[loop1][loop2]/m[loop1][loop2]
                if (tvar>=0 and tvar<=1):
                    ctx.move_to(tvar,0)
                    move_flag = 1
            elif loop3==1: #y=1
                tvar = (1-b[loop1][loop2])/m[loop1][loop2]
                if (tvar>=0 and tvar<=1):
                    if move_flag==0:
                        ctx.move_to(tvar,1)
                        move_flag = 1
                    else:
                        ctx.line_to(tvar,1)
                        break
            elif loop3==2: #x=0
                tvar = b[loop1][loop2]
                if (tvar>=0 and tvar<=1):
                    if move_flag==0:
                        ctx.move_to(0,tvar)
                        move_flag = 1
                    else:
                        ctx.line_to(0,tvar)
                        break
            elif loop3==3: #x=1
                tvar = m[loop1][loop2]+b[loop1][loop2]
                if (tvar>=0 and tvar<=1):
                    if move_flag==0:
                        ctx.move_to(1,tvar)
                        move_flag = 1
                    else:
                        ctx.line_to(1,tvar)
                        break

# Find the intersections of perpendicular bisectors
# then draw a line from the center to these points and
# check if these lines intersect any other bisectors.
for loop1 in range(0,noofcenters):
#for loop1 in range(tidx,tidx+1):
    idx = 0
    for loop2 in range(0, noofcenters):
        if (loop2==loop1):
            continue
        for loop3 in range(loop2+1, noofcenters):
            if (m[loop1][loop3]-m[loop1][loop2])==0:
                continue;
            if (loop3==loop1):
                continue
            # intersection of loop2 and loop3 bisectors
            tempx = (b[loop1][loop2]-b[loop1][loop3])/(m[loop1][loop3]-m[loop1][loop2])
            tempy = m[loop1][loop2]*tempx+b[loop1][loop2]
            if (tempx<0 or tempy<0 or tempx>1 or tempy>1):
                continue
            cand_flag = 1
            len_a=veclen(tempx,tempy,base_x[loop1],base_y[loop1])
            # the line from center to this intersection point
            tempm = (base_y[loop1]-tempy)/(base_x[loop1]-tempx)
            tempb = tempy-tempm*tempx
            for loop4 in range(0,noofcenters):
                if (loop4==loop1 or loop4==loop2 or loop4==loop3):
                    continue
                candx = (b[loop1][loop4]-tempb)/(tempm-m[loop1][loop4])
                candy = tempm*candx+tempb
                len_b=veclen(candx,candy,base_x[loop1],base_y[loop1])
                len_c=veclen(candx,candy,tempx,tempy)
                if (len_a>len_b and len_a>len_c):
                    cand_flag=0
            if cand_flag==1:
                ax[loop1][idx] = tempx
                ay[loop1][idx] = tempy
                idx = idx+1

#print("---------------")
#finding edge nodes
#for loop1 in range(tidx,tidx+1):
for loop1 in range(0,noofcenters):
    idx = 0
    while((ax[loop1][idx]>0 or ay[loop1][idx]>0) and idx<noofcenters+5): #TODO: maxidx
        idx = idx+1
    corner_flag = [0]*4
    for loop2 in range(0, noofcenters):
        if (loop2==loop1):
            continue
        for loop3 in range(0,8):
            if loop3==0: #x=0
                tempx = 0
                tempy = b[loop1][loop2]
            elif loop3==1: #x=1
                tempx = 1
                tempy = m[loop1][loop2]+b[loop1][loop2]
            elif loop3==2: #y=0
                tempx = -b[loop1][loop2]/m[loop1][loop2]
                tempy = 0
            elif loop3==3: #y=1
                tempx = (1-b[loop1][loop2])/m[loop1][loop2]
                tempy = 1
            elif loop3==4: #x=0,y=0
                if corner_flag[3] == 0:
                    tempx = 0
                    tempy = 0
                    corner_flag[0] = 1
                else:
                    continue
            elif loop3==5: #x=1,y=0
                if corner_flag[3] == 0:
                    tempx = 1
                    tempy = 0
                    corner_flag[1] = 1
                else:
                    continue
            elif loop3==6: #x=0,y=1
                if corner_flag[3] == 0:
                    tempx = 0
                    tempy = 1
                    corner_flag[2] = 1
                else:
                    continue
            elif loop3==7: #x=1,y=1
                if corner_flag[3] == 0:
                    tempx = 1
                    tempy = 1
                    corner_flag[3] = 1
                else:
                    continue
            if (tempx<0 or tempy<0 or tempx>1 or tempy>1):
                continue
            #if (loop2>0 and loop3>3):
            #    continue
            cand_flag = 1
            len_a=veclen(tempx,tempy,base_x[loop1],base_y[loop1])
            # the line from center to this intersection point
            tempm = (base_y[loop1]-tempy)/(base_x[loop1]-tempx)
            tempb = tempy-tempm*tempx
            for loop4 in range(0,noofcenters):
                #if (loop4==loop1 or loop4==loop2):
                #    continue
                candx = (b[loop1][loop4]-tempb)/(tempm-m[loop1][loop4])
                candy = tempm*candx+tempb
                len_b=veclen(candx,candy,base_x[loop1],base_y[loop1])
                len_c=veclen(candx,candy,tempx,tempy)
                if (len_a>len_b and len_a>len_c):
                    cand_flag=0
            if cand_flag==1:
                ax[loop1][idx] = tempx
                ay[loop1][idx] = tempy
                idx = idx+1
    Nidx[loop1] = idx

# print("---------------")
# idx = 0
# for loop1 in range(0,nooflines):
#     for loop2 in range(loop1+1,nooflines):
#         # print("-",loop1," " ,loop2," " ,m[loop1]-m[loop2])
#         # print("-",loop1," " ,loop2," " ,b[loop1]-b[loop2])
#         # print(loop1," " ,loop2)
#         # print((b[loop2]-b[loop1])/(m[loop1]-m[loop2]))
#         ax[idx] = (b[loop2]-b[loop1])/(m[loop1]-m[loop2])
#         ay[idx] = m[loop1]*ax[idx]+b[loop1]
#         print(idx," ",ax[idx]," `",ay[idx])
#         ctx.move_to(ax[idx], ay[idx])
#         ctx.arc(ax[idx],ay[idx],0.002, 0, 2*(math.pi))
#         ctx.fill
#         idx = idx+1

# Sorting based on angle
for loop1 in range(0,noofcenters):
#for loop1 in range(3,4):
    print(ax[loop1])
    print(ay[loop1])
    for idx in range(0, Nidx[loop1]):
        tempx = ax[loop1][idx]-base_x[loop1]
        tempy = ay[loop1][idx]-base_y[loop1]
        angle_t[loop1][idx] = math.atan2(tempy, tempx)
        ctx.move_to(ax[loop1][idx], ay[loop1][idx])
        ctx.arc(ax[loop1][idx],ay[loop1][idx],0.01, 0, 2*(math.pi))
        ctx.fill
    for loop2 in range(0, Nidx[loop1]-1):
        for loop3 in range(loop2+1, Nidx[loop1]):
            if angle_t[loop1][loop2]>angle_t[loop1][loop3]:
                tempx = ax[loop1][loop2]
                tempy = ay[loop1][loop2]
                tempang = angle_t[loop1][loop2]
                ax[loop1][loop2] = ax[loop1][loop3]
                ay[loop1][loop2] = ay[loop1][loop3]
                angle_t[loop1][loop2] = angle_t[loop1][loop3]
                ax[loop1][loop3] = tempx
                ay[loop1][loop3] = tempy
                angle_t[loop1][loop3] = tempang
    for idx in range(0, Nidx[loop1]-1):
        ctx.move_to(ax[loop1][idx], ay[loop1][idx])
        ctx.line_to(ax[loop1][idx+1], ay[loop1][idx+1])
    ctx.move_to(ax[loop1][idx+1], ay[loop1][idx+1])
    ctx.line_to(ax[loop1][0], ay[loop1][0])



delta = delta_base
for loop1 in range(0,noofcenters):
#for loop1 in range(3,4):
    print(Nidx[loop1])
    print(ax[loop1])
    print(ay[loop1])
    draw_spiral(ax[loop1], ay[loop1], 0, Nidx[loop1], delta, 0.05, 100)


#ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
ctx.set_line_width(0.002)
ctx.stroke()

surface.write_to_png("vornoi.png")  # Output to PNG
