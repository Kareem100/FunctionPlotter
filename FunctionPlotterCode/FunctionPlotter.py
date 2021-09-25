from tkinter import *
from tkinter import messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
APPLICATION_NAME = "Function Plotter"
USER_INPUT_NOTES = "In (Function field), Please enter a function in terms of only X.\n " \
                   "In (Min X field), Please enter the minimum value of X to be plotted.\n" \
                   "In (Max X field), Please enter the maximum value of X to be plotted."
INVALID_REGEX = "[@_!#$%&<>?|}{~:]"

DEFAULT_FUNCTION = "x^2"
DEFAULT_NEGATIVE_X = -15
DEFAULT_POSITIVE_X = 15
DEFAULT_X_DOMAIN = (-10000, 10000)

# list of allowed operations from user to be evaluated
valid_operations = [
    '+',
    '-',
    '*',
    '/',
    '^'
]


class TkinterFuncPlotter:
    """ Linking between tkinter Widgets and 2D matplotlib plots. """

    def __init__(self):
        # creating main Tkinter window
        self.window = Tk()
        # setting window title
        self.window.title(APPLICATION_NAME)
        # setting app image
        # self.window.iconbitmap('icon.ico')
        # centering tkinter window in screen
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()
        positionTop = int(screenHeight / 2 - WINDOW_HEIGHT / 2)
        positionRight = int(screenWidth / 2 - WINDOW_WIDTH / 2)
        self.window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{positionRight}+{positionTop}')
        # initializing some widgets variables
        self.functionPlot = self.functionEntry = self.plotButton = self.maxXSpinbox = self.minXSpinbox = self.canvas = 0

        # configuring 6 rows by 4 columns (6x4) for widgets
        self.configureGrid()
        # plotting the graph in Tkinter window
        self.plotGraph()
        # plotting the widgets in Tkinter window
        self.plotWidgets()
        # run the gui
        self.window.mainloop()

    def configureGrid(self):
        """ Splitting window into 6x4 grid with custom rows/cols configuration. """
        # configuring first row for Toolbar
        Grid.rowconfigure(self.window, 0, weight=0)
        # configuring second row for Graph
        Grid.rowconfigure(self.window, 1, weight=1)
        # configuring third row for entry and button
        Grid.rowconfigure(self.window, 2, weight=0)
        # configuring fourth row for label and spinbox
        Grid.rowconfigure(self.window, 3, weight=0)
        # configuring fifth row for label and spinbox
        Grid.rowconfigure(self.window, 4, weight=0)
        # configuring sixth row for bottom margin
        Grid.rowconfigure(self.window, 5, weight=0)
        # configuring first column for Toolbar and function label
        Grid.columnconfigure(self.window, 0, weight=0)
        # configuring second column for Graph and function entry
        Grid.columnconfigure(self.window, 1, weight=2)
        # configuring third column for plot button
        Grid.columnconfigure(self.window, 2, weight=2)
        # configuring fourth column for min & max x
        Grid.columnconfigure(self.window, 3, weight=2)

    def plotGraph(self):
        """ Creating the figure that will contain the plot """
        # the figure that will contain the plot
        fig = Figure()
        # adding the subplot
        self.functionPlot = fig.add_subplot(111)
        # creating the Tkinter canvas containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig, self.window)
        self.canvas.draw()
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, padx=10, sticky="news")

        # creating the Matplotlib toolbar
        toolbarFrame = Frame(self.window)
        toolbarFrame.grid(row=0, column=0, columnspan=4, padx=10, sticky="nws")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
        toolbar.update()

    def plotWidgets(self):
        """ Plotting labels, function Entry, button and spinerboxes into Tkinter window
        and onChangeValue Events call. """
        # Function Label
        functionLabel = Label(self.window)
        functionLabel.grid(row=2, column=0, padx=5, sticky="w")
        self.configWidget(functionLabel, text="Function: ", fontSize=14)

        # Function Entry
        self.functionEntry = Entry(self.window)
        self.functionEntry.insert(0, DEFAULT_FUNCTION)
        self.functionEntry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, ipady=4, sticky="we")
        self.configWidget(self.functionEntry, fg="darkgreen")

        # Plot Button
        self.plotButton = Button(self.window, relief="groove", cursor="hand2")
        self.plotButton.grid(row=2, column=3, padx=5, pady=5, ipady=2, sticky="we")
        self.configWidget(self.plotButton, text="P L O T", fg="darkgreen")

        # Min X Label
        minXLabel = Label(self.window)
        minXLabel.grid(row=3, column=0, padx=5, sticky="e")
        self.configWidget(minXLabel, text="Min X: ")
        # Min X spinbox
        defaultMinValue = StringVar(self.window)
        defaultMinValue.set(DEFAULT_NEGATIVE_X)
        self.minXSpinbox = Spinbox(self.window, from_=DEFAULT_X_DOMAIN[0], to=DEFAULT_X_DOMAIN[1],
                                   textvariable=defaultMinValue)
        self.minXSpinbox.grid(row=3, column=1, columnspan=1, padx=5, pady=5, ipady=2, sticky="we")
        self.configWidget(self.minXSpinbox, text="Min X: ", fg="darkgreen")

        # Max X Label
        maxXLabel = Label(self.window, text="Max X: ")
        maxXLabel.grid(row=4, column=0, padx=5, sticky="e")
        self.configWidget(maxXLabel, text="Max X: ")
        # Max X spinbox
        defaultMaxValue = StringVar(self.window)
        defaultMaxValue.set(DEFAULT_POSITIVE_X)
        self.maxXSpinbox = Spinbox(self.window, from_=DEFAULT_X_DOMAIN[0], to=DEFAULT_X_DOMAIN[1],
                                   textvariable=defaultMaxValue)
        self.maxXSpinbox.grid(row=4, column=1, columnspan=1, padx=5, pady=5, ipady=2, sticky="we")
        self.configWidget(self.maxXSpinbox, text="Max X: ", fg="darkgreen")

        # User Input Notes Label
        message = Label(self.window, bd=1, relief="groove", bg="beige", justify="center")
        message.grid(row=3, column=2, rowspan=2, columnspan=2, padx=5, pady=5, ipady=2, sticky="news")
        self.configWidget(message, text=USER_INPUT_NOTES, fg="crimson", fontSize=8)

        # Bottom Margin as a Label
        Label(self.window).grid(row=5, column=0, columnspan=4, padx=5, pady=5, ipady=2, sticky="we")

        # Adding on Value Changes Events
        self.onValueChange(0)
        self.minXSpinbox.configure(command=lambda: self.onValueChange(ID=1))
        self.maxXSpinbox.configure(command=lambda: self.onValueChange(ID=2))
        self.plotButton.configure(command=lambda: self.onValueChange(ID=3))

    @staticmethod
    def configWidget(widget, text="", fontSize=10, fg="black", highlightColor="royalblue", highlightThickness=1):
        """ Passing the most repeated attributes among different widgets. """
        widget.configure(text=text, font=('Helvetica', fontSize, 'bold'), fg=fg,
                         highlightthickness=highlightThickness, highlightcolor=highlightColor)

    def onValueChange(self, ID):
        # ID  -> determines what widget changed
        """ Update the plot with the newly changed values. """
        minX = int(self.minXSpinbox.get())
        maxX = int(self.maxXSpinbox.get())

        # Validating minX can't be greater than or equal to maxX
        if ID == 1 and minX >= maxX:
            messagebox.showerror("MAX X EXCEEDS IT'S LIMITS !", "'Max X' should be less than 'Min X' !!")
            minX = StringVar(self.window)
            minX.set(maxX - 1)
            self.minXSpinbox.config(textvariable=minX)
            return

        # Validating: max x can't be less than or equal to min x
        if ID == 2 and maxX <= minX:
            messagebox.showerror("MIN X EXCEEDS IT'S LIMITS !", "'Min X' should not be greater than 'Max x' !!")
            maxX = StringVar(self.window)
            maxX.set(minX + 1)
            self.maxXSpinbox.config(textvariable=maxX)
            return

        xPoints = np.linspace(minX, maxX)
        try:
            fx = self.translateToFunction(self.functionEntry.get())(xPoints)
        except ValueError as e:
            messagebox.showerror("Invalid Input Function !", str(e))
            return

        # plotting the graph function
        self.functionPlot.clear()
        self.functionPlot.plot(xPoints, fx)
        self.canvas.draw()

    @staticmethod
    def translateToFunction(inputString):
        """ Evaluate the input string and return a valid function. """

        # Searching for suspicious (invalid) input
        for ch in inputString:
            if ch in INVALID_REGEX or (ch.isalpha() and ch != 'x' and ch != 'X'):
                raise ValueError(
                    f"'{ch}' is not allowed to be used in this math expression.\n"
                    f"Only functions of 'x' are allowed.\ne.g., 2*x^2 + 4/x - 3\n\n"
                    f"Please use one of these: x, {', '.join(valid_operations)}"
                )

        # handling power operator and capitalized x variable
        inputString = inputString.replace('^', '**')
        inputString = inputString.replace('X', 'x')
        for i in range(len(inputString)-1):
            if inputString[i] == 'x' and inputString[i+1] == 'x':
                raise ValueError(
                    f"'xx' is not allowed to be used in this math expression.\n"
                    f"It's a tedious operation.\n\n"
                    f"Please use one of these between two X's: {', '.join(valid_operations)}"
                )
        # handling constant functions e.g., f(x) = 5
        if "x" not in inputString:
            inputString = f"0*x+{inputString}"

        def fun(x):
            try:
                return eval(inputString)
            except SyntaxError as e:
                raise ValueError(
                    "Wrong Mathematical Function.\nPlease Check Your Input.\n"
                )

        return fun


if __name__ == "__main__":
    # main entry point
    TkinterFuncPlotter()
