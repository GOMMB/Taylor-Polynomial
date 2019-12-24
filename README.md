## Requirements

Required Python modules include: SymPy, Tkinter, Matplotlib, and NumPy

## Usage

When you run the program, you will be prompted with a dialog box where you will input your parameters.
* **Minimum/Maximum**: The graph will plot the range of x values between minimum and maximum. Note that if values are included that aren't in the domain of the function, the program may crash.
* **Resolution**: This is the number of vertices that will be plotted, and therefore a higher resolution will result in a smoother graph.
* **f(x)**: This is the function that will be plotted and approximated using Taylor polynomials.
Click "OK" or press Enter to proceed from this dialog box.

You will then be displayed with the graph and another dialog box. The graph will display both the original function (in blue) and the Taylor polynomial (in orange).

The new dialog box contains sliders that you can manipulate to change the Taylor polynomial.
* **Degree**: This is the degree of the Taylor polynomial, and so generally speaking, the higher the degree, the better the approximation.
* **Base**: This is the base of the Taylor polynomial, commonly just refrenced as <i>b</i>. Adjusting this moves the Taylor polynimal accross the original function.
