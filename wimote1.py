import time
import cwiid
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy

max_points = 500

print('** Connecting wiimote **')
wm = cwiid.Wiimote()
wm.led = 15
wm.rpt_mode = cwiid.RPT_IR
print('** Connected **')

plt.axis([0,1000,0,800])

# plt.ion()     # turns on interactive mode

fig = plt.figure(1)
ax = fig.add_subplot()
ax.axis([0,1000,0,800])

xpoints = [50]
ypoints = [50]

plot, = ax.plot(xpoints, ypoints, color='black', markersize=1, marker='o', linestyle='')

def update(point):
  x,y = point

  if x == 0 and y == 0: return plot

  xps, yps = plot.get_data()

  newXps = numpy.append(xps, x)
  newYps = numpy.append(yps, y)

  if len(newYps) > max_points:
    newXps = numpy.delete(newXps, 0)        
    newYps = numpy.delete(newYps, 0)      

  plot.set_data(newXps, newYps)

  return plot

def getPoint():
  while True:
    # st = time.time()
    point = wm.state['ir_src'][0]
    # print(time.time() - st)

    if point is None:
      yield 0,0
    else:
      x,y = point['pos']
      yield x,y

anim = animation.FuncAnimation(fig, update, getPoint, interval=500)

plt.show()
# frames_buffer = 0
# should_draw = False

# while True:
#   point1 = wm.state['ir_src'][0]

#   if point1 is not None:
#     x,y = point1['pos']
#     xpoints.append(x)
#     ypoints.append(y)

    # if len(xpoints) > max_points:
    #   xpoints.pop(0)
    #   ypoints.pop(0)

#     should_draw = frames_buffer % buffer_length == 0 and frames_buffer != 0
#     frames_buffer += 1

#     if (should_draw):
#       frames_buffer = 0
#       plot.set_data(xpoints, ypoints)    
#       plt.draw()
#       plt.pause(0.001)

#     # print(f'points: {len(xpoints)}, buffer: {frames_buffer}, draw: {should_draw}, firstpoint: {xpoints[0]},{ypoints[0]}')

#   time.sleep(0.001)

# time.sleep(10)