import time
import cwiid
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from multiprocessing import Process, Manager, Lock

lock = Lock()

def updater(xps, yps, lock):
  maxpoints = 30

  print('** Connecting wiimote **')
  wm = cwiid.Wiimote()
  wm.led = 15
  wm.rpt_mode = cwiid.RPT_IR
  print('** Connected **')
  
  while True:
    lock.acquire()

    point = wm.state['ir_src'][0]
    if point is not None:
      x,y = point['pos']
      if len(xps) > maxpoints:
        xps.pop(0)
        yps.pop(0)
      xps.append(-x)
      yps.append(-y)
    
    lock.release()

    time.sleep(0.05)

def main():
  with Manager() as manager:
    xpoints = manager.list([])
    ypoints = manager.list([])

    fig, ax = plt.subplots()
    
    plt.axis([-1024,0,-768,0])
    ax.axis([-1024,0,-768,0])

    line, = ax.plot(xpoints, ypoints, color='black', marker='', linestyle='-', linewidth=3, solid_joinstyle='round')

    def animate(_):
      lock.acquire()
      
      newx = np.array(xpoints)
      newy = np.array(ypoints)

      line.set_data(newx, newy)
      
      lock.release()
      
      return line,

    p1 = Process(target=updater, args=[xpoints, ypoints, lock])
    
    p1.start()

    ani = animation.FuncAnimation(fig, animate, interval=33, blit=True, save_count=30)

    plt.show()

    p1.join()

if __name__ == '__main__':
  main()
