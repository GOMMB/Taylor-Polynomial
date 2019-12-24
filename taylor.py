import sympy
from sympy.core.sympify import sympify
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from threading import Thread
from queue import Queue

master = tk.Tk()

master.geometry('300x150')

tk.Label(master, text="Minimum").grid(row=0)
tk.Label(master, text="Maximum").grid(row=1)
tk.Label(master, text="Resolution").grid(row=2)
tk.Label(master, text="f(x) = ").grid(row=3)

minEntry = tk.Entry(master, width=9)
minEntry.insert(0, -10)
maxEntry = tk.Entry(master, width=9)
maxEntry.insert(0, 10)
resEntry = tk.Entry(master, width=9)
resEntry.insert(0, 1000)
funcEntry = tk.Entry(master, width=9)
funcEntry.insert(0, 'sin(x)')

minEntry.grid(row=0, column=1)
maxEntry.grid(row=1, column=1)
resEntry.grid(row=2, column=1)
funcEntry.grid(row=3, column=1)


def on_closing():
    global min, max, res, func
    min = float(minEntry.get())
    max = float(maxEntry.get())
    res = int(resEntry.get())
    func = sympify(funcEntry.get().replace('e', '2.718281828459045'))
    master.destroy()

	
def enter_pressed(event):
    on_closing()
	

tk.Button(master, text='OK', command=on_closing).grid(row=4, column=0)

master.bind("<Return>", enter_pressed)
master.protocol("WM_DELETE_WINDOW", lambda: exit())
master.title("Taylor Approximation")

master.mainloop()

data = Queue()

def slider_thread(min, max):
    global slider

    def changed(*args):
        data.put(('d', slider.get()))

    def changed_base(*args):
        data.put(('b', base.get()))

    taylor_degree = tk.Tk()
	
    tk.Label(taylor_degree, text="Degree:").grid(row=0)
	
    slider = tk.IntVar()
    slider.trace('w', changed)
    scale = tk.Scale(taylor_degree, from_=1, to=100, orient=tk.HORIZONTAL, length=300, variable=slider)
    scale.grid(row=1)
	
    tk.Label(taylor_degree, text="Base:").grid(row=2)
	
    base = tk.DoubleVar()
    base.trace('w', changed_base)
    scale_base = tk.Scale(taylor_degree, from_=min, to=max, orient=tk.HORIZONTAL, length=300, resolution=0.5, variable=base)
    scale_base.grid(row=3)
    base.set((min + max) / 2)

    taylor_degree.protocol("WM_DELETE_WINDOW", lambda: exit())
    taylor_degree.title("Taylor Polynomial Degree and Base")

    taylor_degree.mainloop()


Thread(target=slider_thread, args=[min, max], daemon=True).start()

x_sym = sympy.Symbol('x')
b = sympy.Symbol('b')
derivatives = [func]
terms = [func.subs(x_sym, b)]

def get_derivatives(n):
    while len(derivatives) - 1 < n:
        derivatives.append(derivatives[-1].diff(x_sym))
    if len(terms) - 1 < n:
        for i in range(len(terms), len(derivatives)):
            terms.append((derivatives[i].subs(x_sym, b) / sympy.factorial(i)) * (x_sym - b) ** i)


x = np.linspace(min, max, res)
y = sympy.lambdify(x_sym, func, 'numpy')(x)

fig = plt.figure()
ax = plt.axes()
curve1, = ax.plot(x, y)
curve2, = ax.plot([], [])

def update_curve(degree, base):
    get_derivatives(degree)
    polynomial_func = sum(terms[0:degree+1])
    deriv = sympy.lambdify(x_sym, polynomial_func.subs(b, base), 'numpy')
    curve2.set_data(x, deriv(x))
    return curve1, curve2,


def animate(i):
    global degree, base
    if data.empty():
        return curve1, curve2,

    while not data.empty():
        k, v = data.get()
        if k == 'd':
            degree = v
        else:
            base = v

    return update_curve(degree, base)


anim = FuncAnimation(fig, animate, blit=True, interval=20)

plt.show()
