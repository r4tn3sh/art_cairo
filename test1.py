#!/usr/bin/python3
import math
import cairo
import random

WIDTH, HEIGHT = 1024, 1024

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
ctx.set_line_width(0.01)

min_x = 0.3
max_x = 0.7
delta_base = 0.05
edge_x = [0]*5 #assuming 4 edges
edge_y = [0]*5

#random.seed(1)
# Get 4 random coordinates for 4 edges
a1 = random.uniform(min_x, max_x)
a2 = random.uniform(min_x, max_x)
a3 = random.uniform(min_x, max_x)
a4 = random.uniform(min_x, max_x)

# Choose a random center point
bx = random.uniform(min_x, max_x)
by = random.uniform(min_x, max_x)

## quadrant 0
qd = 0
ctx.move_to(a1, 0)
ctx.line_to(bx, by)
# edges of this quadrant
edge_x[0]=0
edge_y[0]=0
edge_x[1]=a1
edge_y[1]=0
edge_x[2]=bx
edge_y[2]=by
edge_x[3]=0
edge_y[3]=a2
ctx.move_to(edge_x[0], edge_y[0])
delta = delta_base
for loop in range(0,100):
	idx = (loop)%4
	#print("------------------")
	#print(edge_x[idx], " ", edge_y[idx])
	#print(edge_x[(idx+1)%4], " ", edge_y[(idx+1)%4])
	#print(edge_x[(idx+2)%4], " ", edge_y[(idx+2)%4])
	nxt_x = edge_x[(idx+1)%4]*(1-delta) + edge_x[(idx+2)%4]*delta
	nxt_y = edge_y[(idx+1)%4]*(1-delta) + edge_y[(idx+2)%4]*delta
	#print(nxt_x, " ", nxt_y)
	edge_x[(idx+1)%4] = nxt_x
	edge_y[(idx+1)%4] = nxt_y
	ctx.line_to(nxt_x, nxt_y)
	delta = min(1.05*delta, 0.5)
	#print (delta)
	#ctx.close_path()

## quadrant 1
ctx.move_to(0, a2)
ctx.line_to(bx, by)  # Line to (x,y)
# edges of this quadrant
edge_x[0]=0
edge_y[0]=1
edge_x[1]=0
edge_y[1]=a2
edge_x[2]=bx
edge_y[2]=by
edge_x[3]=a3
edge_y[3]=1
ctx.move_to(edge_x[0], edge_y[0])
delta = delta_base
for loop in range(0,100):
	idx = (loop)%4
	nxt_x = edge_x[(idx+1)%4]*(1-delta) + edge_x[(idx+2)%4]*delta
	nxt_y = edge_y[(idx+1)%4]*(1-delta) + edge_y[(idx+2)%4]*delta
	edge_x[(idx+1)%4] = nxt_x
	edge_y[(idx+1)%4] = nxt_y
	ctx.line_to(nxt_x, nxt_y)
	delta = min(1.05*delta, 0.5)

ctx.move_to(a3, 1)
ctx.line_to(bx, by)  # Line to (x,y)
# edges of this quadrant
edge_x[0]=1
edge_y[0]=1
edge_x[1]=a3
edge_y[1]=1
edge_x[2]=bx
edge_y[2]=by
edge_x[3]=1
edge_y[3]=a4
ctx.move_to(edge_x[0], edge_y[0])
delta = delta_base
for loop in range(0,100):
	idx = (loop)%4
	nxt_x = edge_x[(idx+1)%4]*(1-delta) + edge_x[(idx+2)%4]*delta
	nxt_y = edge_y[(idx+1)%4]*(1-delta) + edge_y[(idx+2)%4]*delta
	edge_x[(idx+1)%4] = nxt_x
	edge_y[(idx+1)%4] = nxt_y
	ctx.line_to(nxt_x, nxt_y)
	delta = min(1.05*delta, 0.5)

ctx.move_to(1, a4)
ctx.line_to(bx, by)  # Line to (x,y)
# edges of this quadrant
edge_x[0]=1
edge_y[0]=0
edge_x[1]=1
edge_y[1]=a4
edge_x[2]=bx
edge_y[2]=by
edge_x[3]=a1
edge_y[3]=0
ctx.move_to(edge_x[0], edge_y[0])
delta = delta_base
for loop in range(0,100):
	idx = (loop)%4
	nxt_x = edge_x[(idx+1)%4]*(1-delta) + edge_x[(idx+2)%4]*delta
	nxt_y = edge_y[(idx+1)%4]*(1-delta) + edge_y[(idx+2)%4]*delta
	edge_x[(idx+1)%4] = nxt_x
	edge_y[(idx+1)%4] = nxt_y
	ctx.line_to(nxt_x, nxt_y)
	delta = min(1.05*delta, 0.5)



#ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
ctx.set_line_width(0.002)
ctx.stroke()

surface.write_to_png("example.png")  # Output to PNG
