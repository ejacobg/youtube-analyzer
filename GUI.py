# Import Modules
import tkinter as tk
from tkinter import * #basic tinker import library 
from tkinter import filedialog #allows files to be explored 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #allows graph to be on window 
from matplotlib.figure import Figure #same as above  
import customtkinter #allows for color customization  
import pandas as pd #library used for data 
import matplotlib.pyplot as plt #library used for making graphs 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Allows graphs to be removed in tkinder window 
from menu import degree_distribution_gui
import os #allows users to navigate around directories 

#functions from other Python files 
from degrees import write_degrees
from menu import input_file
from menu import generate_statistics
from read import read_file

#global variable for window visuals 
root = customtkinter.CTk() #Load window 
buttonSize = 70 #size of button via enhanced font  


#global variables for color customization for buttons 
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



#main function for GUI functionality 
def main():
    window()
    

def dropdownClicked(column, df, entry):
    print("dropdownClicked called!")
    
    # Create a new window for the graph
    newWindow = tk.Tk()
    newWindow.title("Histogram of " + column)
    
    print(f"The '{column}' button was pressed!")
    
    #Aided by (https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/)    
    # Create the figure and axis objects
    fig, ax = plt.subplots(figsize=(6,4), dpi=100)

    print(entry)
    # Create a histogram of the selected column
    ax.hist(df[column], bins=entry)

    # Set the title and axis labels
    ax.set_title("Histogram of " + column)
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    #Create a canvas to display the figure
    canvas = FigureCanvasTkAgg(fig, master=newWindow)
    canvas.draw()
    canvas.get_tk_widget().pack()

    

#plot function to plot CSV data 
def plotFile(userFile):
    
    PlotWindow = tk.Tk() #new window 
    PlotWindow.title("Plot Customization") #title 
    PlotWindow.geometry('500x300') # Window size
    
    print(userFile)
    #check if file chosen is a CSV 
    if userFile.endswith('.csv'):
        
        #Read the CSV file
        df = pd.read_csv(userFile)    

        #Get column information from CSV
        columnNames = df.columns.tolist()

       
        #slider function to set global variable 
        def slider_event(value):
            slider_value.set(value)
            label.config(text="bin number: " + str(slider_value.get()))

        slider_value = tk.IntVar()
        slider = customtkinter.CTkSlider(master=PlotWindow, number_of_steps=20, from_=0, to=20, command=slider_event)
        slider.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label = tk.Label(PlotWindow, text="bin number: " + str(slider_value.get()), font='Arial 12 bold')
        label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        # Create a dropdown for each column in the CSV file 
        combobox = customtkinter.CTkOptionMenu(master=PlotWindow,
                                        values=columnNames,
                                        command=lambda col: dropdownClicked(col, df, slider_value.get()))
        combobox.pack(padx=50, pady=30)
        
    #If not a CSV 
    else:
       # Create text at center of screen to inform user that this is not a CSV
        label=Label(PlotWindow, text="Not a csv file, please try again", font='Arial 12 bold')
        label.place(relx=0.5, rely=0.5, anchor=CENTER)

#replicates degree functionality in CLI 
def degreeFunctionality(df):
    DegreeWindow = tk.Tk()
    DegreeWindow.title("Degree Output Creation")
    DegreeWindow.geometry('1000x600') # Window size

    outputPath = ""

    def degreeDestination(df):    
        outputPath = directorySelection()
        if os.path.isdir(outputPath):
            
            write_degrees(df, outputPath) # pass DataFrame object to write_degrees() function 
            
            label = tk.Label(DegreeWindow, text="Completed! You may now close this window.", font='Arial 14 bold')
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Destroy button after function finishes executing
            buttonInput.destroy()
    
    #button that requires user to select valid input file 
    buttonInput = customtkinter.CTkButton(DegreeWindow, font=("Helvetica", buttonSize), text="Choose Output File", command=lambda: degreeDestination(df))
    buttonInput.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
   
   
#categorized functionality from CLI 
def categorizedFunctionality(df):
    CategorizedWindow = tk.Tk()
    CategorizedWindow.title("Categorize Data")
    CategorizedWindow.geometry('1000x600') # Window size
  
    userInput = '' 
    
    def get_input(df):
        # Get the input from the box
        userInput = input_box.get_text()
        if(userInput != ''):
            df = df.filter(condition)
            button.destory()
            showMenu()

    def showMenu():
        button1 = customtkinter.CTkButton(root,  font=("Helvetica", buttonSize), text="Generate statistics", command=lambda: generate_statistics(df))
        button1.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        button2 = customtkinter.CTkButton(root,  font=("Helvetica", buttonSize), text="Export", command=lambda: degreeFunctionality(df))
        button2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    # Create a button to get the input
    button = customtkinter.CTkButton(CategorizedWindow, text="Type Filter Command", command=get_input(df))
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    button.pack(pady=20)





    
    
   
#function that allows user to browse file nad choose a path 
def fileSelection():
    inputPath = filedialog.askopenfilename() #Allows user to browse their files 
    return inputPath #return file path 

def directorySelection():
    outputPath = filedialog.askdirectory() #Allows uer to browse their directories   
    return outputPath #return directory path 

#Function to load window 
#Aided by (https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/) 
def window():
    
    #root window basics 
    root.title("Youtube Analyzer | Team One | CS 631") # Window title 
    root.geometry('1000x600') # Window size
    
    #Window Menu Declarations  
    menu = Menu(root) #make a menu for the root window  
    flieMenu = Menu(menu) #assign instance of menu to a variable to add functionality 
    root.config(menu=menu) #set menu to be on top layer of window 

    inputPath = "" #input file path 

    #function that uses input file path 
    def Fileinput():
        inputPath = fileSelection()
        if(inputPath.endswith(".txt") or inputPath.endswith(".csv")):
            showMenu(inputPath)
            
            
    #menu from CLI 
    def showMenu(inputPath):
        
        # Load DataFrame from file path
        df = read_file(inputPath).dropna()
    
        # create four buttons with labels and grid positions
        button1 = customtkinter.CTkButton(root,  font=("Helvetica", buttonSize), text="Degree", command=lambda: degreeFunctionality(df))
        button1.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        button2 = customtkinter.CTkButton(root,  font=("Helvetica", buttonSize), text="Categorized Statistics", command=lambda: categorizedFunctionality(df))
        button2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        button3 = customtkinter.CTkButton(root,  font=("Helvetica", buttonSize), text="Plot Graph", command=lambda: plotFile(inputPath))
        button3.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    #button that requires user to select valid input file 
    button0 = customtkinter.CTkButton(root, font=("Helvetica", buttonSize), text="Choose Input File (csv or txt)", command=Fileinput)
    button0.place(relx=0.5, rely=0.1, anchor=tk.CENTER)


    # all widgets will be here
    # Execute Tkinter
    root.mainloop()



if __name__ == "__main__":
    main()
