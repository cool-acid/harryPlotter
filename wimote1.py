import time
import cwiid
import matplotlib.pyplot as plt

buffer_length = 100
max_points = 500

print('** Connecting wiimote **')
wm = cwiid.Wiimote()
wm.led = 15
wm.rpt_mode = cwiid.RPT_IR
print('** Connected **')

plt.axis([0,1000,0,800])

plt.ion()     # turns on interactive mode
plt.show()    # now this should be non-blocking

plt.plot(0, 0, markersize=0.1)
plt.draw()
plt.pause(0.001)
fig = plt.figure(1)
ax = fig.add_subplot()
ax.axis([0,1000,0,800])

xpoints = [0]
ypoints = [0]

plot, = ax.plot(xpoints, ypoints, color='black', markersize=1, marker='o', linestyle='')

frames_buffer = 0
should_draw = False

while True:
  point1 = wm.state['ir_src'][0]

  if point1 is not None:
    x,y = point1['pos']
    xpoints.append(x)
    ypoints.append(y)

    if len(xpoints) > max_points:
      xpoints.pop(0)
      ypoints.pop(0)

    should_draw = frames_buffer % buffer_length == 0 and frames_buffer != 0
    frames_buffer += 1

    if (should_draw):
      frames_buffer = 0
      plot.set_data(xpoints, ypoints)    
      plt.draw()
      plt.pause(0.001)

    # print(f'points: {len(xpoints)}, buffer: {frames_buffer}, draw: {should_draw}, firstpoint: {xpoints[0]},{ypoints[0]}')

  time.sleep(0.001)

