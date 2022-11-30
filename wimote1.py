import cwiid
import matplotlib.pyplot as plt

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

# fig = plt.figure(1)

xpoints = []
ypoints = []

while True:
  point1 = wm.state['ir_src'][0]

  if point1 is not None:
    # print(point1)
    x,y = point1['pos']
    size = point1['size']
    # print(x, y)

    plt.plot(x, y, color='black', marker='o', markersize=size)
    plt.draw()
    plt.pause(0.001)
