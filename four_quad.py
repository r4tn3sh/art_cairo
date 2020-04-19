#!/usr/bin/python3

# This script is only for the case where the area is 
# divided in four quadrants, and sprials can be created
# with different rotation in each quad
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

def draw_spiral(edge_x, edge_y, rot, M, delta, deltainc, N):
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
delta = delta_base
draw_spiral(edge_x, edge_y, 1, 4, delta, 0.05, 100)

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
draw_spiral(edge_x, edge_y, 0, 4, delta, 0.05, 100)

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
draw_spiral(edge_x, edge_y, 1, 4, delta, 0.05, 100)

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
draw_spiral(edge_x, edge_y, 0, 4, delta, 0.05, 100)



#ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
ctx.set_line_width(0.002)
ctx.stroke()

surface.write_to_png("example.png")  # Output to PNG
