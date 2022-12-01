import time
import cwiid
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import numpy as np
from multiprocessing import Process, Manager, Lock

lock = Lock()

def updater(xps, yps, lock, killsig):
  maxpoints = 30

  print('** Connecting wiimote **')
  wm = cwiid.Wiimote()
  wm.led = 15
  wm.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
  print('** Connected **')
  
  while True:
    lock.acquire()

    if wm.state['buttons'] > 0:
      killsig.value = True
    else:
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
  print(matplotlib.get_backend())
  with Manager() as manager:
    xpoints = manager.list([])
    ypoints = manager.list([])
    killsig = manager.Value(False, False)

    fig = plt.figure()
    ax = fig.add_subplot()
    
    plt.axis([-1024,0,-768,0])
    ax.axis([-1024,0,-768,0])
    line, = ax.plot([],[], color='black', marker='', linestyle='-', linewidth=3, solid_joinstyle='round')

    def init():
      line.set_data(xpoints, ypoints)
      return line,

    def animate(_):
      lock.acquire()
      
      newx = np.array(xpoints)
      newy = np.array(ypoints)

      line.set_data(newx, newy)
      
      lock.release()
      
      return line,

    def generator():
      while not killsig.value:
        yield 

      plt.savefig('fig.png', backend='Agg')
      plt.close(fig)
      return 

    p1 = Process(target=updater, args=[xpoints, ypoints, lock, killsig])
    
    p1.start()

    ani = animation.FuncAnimation(fig, animate, generator, interval=33, blit=True, init_func=init)

    plt.show()

    p1.kill()

if __name__ == '__main__':
  main()
