import time
import cwiid
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from multiprocessing import Process, Value, Array, Manager, Lock

lock = Lock()

def test(xps, yps, lock):
  while True:
    lock.acquire()

    last = xps[len(xps) - 1] + 1
    xps.pop(0)
    yps.pop(0)
    xps.append(last)
    yps.append(last)
    
    lock.release()

    print('>', xps, ' ', yps)
    time.sleep(0.05)

# def main():
#   with Manager() as manager:
  
#     lock = Lock()

#     max_points = 500

#     xpoints = manager.list([1,2,3,4,5,6,7,8])
#     ypoints = manager.list([1,2,3,4,5,6,7,8])
    
#     print('** Connecting wiimote **')
#     # wm = cwiid.Wiimote()
#     # wm.led = 15
#     # wm.rpt_mode = cwiid.RPT_IR
#     print('** Connected **')

#     plt.axis([0,1000,0,800])

#     fig = plt.figure(1)
#     ax = fig.add_subplot()
    # ax.axis([0,1000,0,800])

#     plot, = ax.plot(xpoints, ypoints, color='black', markersize=1, marker='o', linestyle='')

#     def update(point):
#       print('point', point)
#       # x,y = point

#       # if x == 0 and y == 0: return plot

#       # xps, yps = plot.get_data()



#       # newXps = numpy.append(xps, x)
#       # newYps = numpy.append(yps, y)

#       # if len(newYps) > max_points:
#       #   newXps = numpy.delete(newXps, 0)        
#       #   newYps = numpy.delete(newYps, 0)      

#       lock.acquire()
#       # print('<', xpoints, ' ', ypoints)
#       plot.set_data(xpoints, ypoints)
#       lock.release()

#       return plot

#     def getPoint():
#       while True:
#         # st = time.time()
#         # point = wm.state['ir_src'][0]
#         point = None
#         # print(time.time() - st)

#         if point is None:
#           yield 0,0
#         else:
#           x,y = point['pos']
#           yield x,y

    # p1 = Process(target=test, args=[xpoints, ypoints, lock])
    
    # p1.start()
    
#     anim = animation.FuncAnimation(fig, update, interval=10)

#     plt.show()

#     p1.join()
def main():
  with Manager() as manager:
    xpoints = manager.list([1,2,3,4,5,6,7,8])
    ypoints = manager.list([1,2,3,4,5,6,7,8])

    fig, ax = plt.subplots()
    
    plt.axis([0,1000,0,800])
    ax.axis([0,1000,0,800])

    line, = ax.plot(xpoints, ypoints)

    def animate(_):
      # newx = xpoints.append(xpoints[len(xpoints) - 1])
      # newy = ypoints.append(ypoints[len(ypoints) - 1])
      # line.set_data(np.array(newx), np.array(newy))  # update the data.
      lock.acquire()
      
      newx = np.array(xpoints)
      newy = np.array(ypoints)

      line.set_data(newx, newy)
      
      lock.release()
      
      return line,

    p1 = Process(target=test, args=[xpoints, ypoints, lock])
    
    p1.start()

    ani = animation.FuncAnimation(fig, animate, interval=10, blit=True, save_count=50)

    plt.show()

    p1.join()

if __name__ == '__main__':
  main()
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
