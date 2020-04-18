#!/usr/bin/python3
import math
import cairo
import random

WIDTH, HEIGHT = 512, 512

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
ctx.set_line_width(0.01)

min_x = 0.3
max_x = 0.7
delta = 0.05
edge_x = [0]*5 #assuming 4 edges
edge_y = [0]*5
xfctr = [1, -1, -1, 1]
yfctr = [1, 1, -1, -1]

random.seed(1)
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
for loop in range(0,50):
	idx = (loop)%4
	nxt_x = edge_x[(idx+1)%4]*(1-delta) + xfctr[(idx+qd)%4]*edge_x[(idx+2)%4]*delta
	nxt_y = edge_y[(idx+1)%4]*(1-delta) + yfctr[(idx+qd)%4]*edge_y[(idx+2)%4]*delta
	edge_x[(idx+1)%4] = nxt_x
	edge_y[(idx+1)%4] = nxt_y
	ctx.line_to(nxt_x, nxt_y)
	#ctx.close_path()

ctx.move_to(0, a2)
ctx.line_to(bx, by)  # Line to (x,y)
ctx.move_to(a3, 1)
ctx.line_to(bx, by)  # Line to (x,y)
ctx.move_to(1, a4)
ctx.line_to(bx, by)  # Line to (x,y)


#ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
ctx.set_line_width(0.005)
ctx.stroke()

surface.write_to_png("example.png")  # Output to PNG
