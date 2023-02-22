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

#global variable for window 
root = customtkinter.CTk() #Load window

#global variables for color customization for buttons 
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



#main function for GUI functionality 
def main():
    window()
    

def dropdownClicked(column, df):
    print("dropdownClicked called!")
    
    # Create a new window for the graph
    newWindow = tk.Tk()
    newWindow.title("Histogram of " + column)
    
    print(f"The '{column}' button was pressed!")
    
    #Aided by (https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/)    
    # Create the figure and axis objects
    fig, ax = plt.subplots(figsize=(6,4), dpi=100)

    # Create a histogram of the selected column
    ax.hist(df[column], bins=7)

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
    #check if file chosen is a CSV 
    if userFile.endswith('.csv'):
        
        #Read the CSV file
        df = pd.read_csv(userFile)    

        #Get column information from CSV
        columnNames = df.columns.tolist()

        #Create a dropdown for each column in the CSV file 
        #aided by (https://github.com/TomSchimansky/CustomTkinter/wiki/CTkButton)
        combobox = customtkinter.CTkOptionMenu(master=root,
                                        values=columnNames,
                                        command=lambda col: dropdownClicked(col, df))
        combobox.pack(padx=50, pady=30)

    #If not a CSV 
    else:
       # Create text at center of screen to inform user that this is not a CSV
        label=Label(root, text="Not a csv file, please try again", font='Arial 12 bold')
        label.place(relx=0.5, rely=0.5, anchor=CENTER)



#Function to load window 
#Aided by (https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/) 
def window():
    
    #root window basics 
    root.title("Youtube Analyzer | Team One | CS 631") # Window title 
    root.geometry('1000x600') # Window size
    

    #function that allows user to browse file nad choose a path 
    def chooseFile():
        filePath = filedialog.askopenfilename() #Allows user to browse their directories 
        return filePath 

    #Window Menu Declarations  
    menu = Menu(root) #make a menu for the root window  
    flieMenu = Menu(menu) #assign instance of menu to a variable to add functionality 
    root.config(menu=menu) #set menu to be on top layer of window 

    #Root Menu Options 
    menu.add_cascade(label='File', menu=flieMenu) #Button at top menu  
    flieMenu.add_command(label='Open', command=lambda: plotFile(chooseFile())) #option within button that calls chooseFile() 
    #Note lambda here means that chooseFile() will have to return something first then plot_file() will be executed.
    #Without lambda the the functions might be executed simultaneously or without waiting for chooseFile()


    #testing 

    sizing = 70 #size of button via enhanced font  
    
    # create four buttons with labels and grid positions
    button1 = customtkinter.CTkButton(root,  font=("Helvetica", sizing), text="Degree")
    button1.grid(column=0, row=0, sticky="S",  pady=20)

    button2 = customtkinter.CTkButton(root,  font=("Helvetica", sizing), text="Categorized Statistics")
    button2.grid(column=0, row=1, sticky="N", pady=20)

    # center the buttons in the window
    root.columnconfigure(0, weight=1)
    root.rowconfigure([0, 1], weight=1)

    # all widgets will be here
    # Execute Tkinter
    root.mainloop()



if __name__ == "__main__":
    main()
