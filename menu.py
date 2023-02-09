import os


def menu_options(command):
    if command == "D":
        path = get_file("Input output directory:")
		 
        print("Writing to ", path)
		
        print("[Call function to degrees]")

        print("Finished")
		
        menu_display()

    if command == "C": 
        print("Filter data:")
		

        user_input = False
        subcommand = " "
        while not (subcommand == "G" or subcommand == "E" or subcommand == "B"):
            print("===Menu===\n [G]enerate statistics\n [E]xport\n [B]ack")
            subcommand = input("Enter Command:")
           
            if (subcommand == "G" or subcommand == "B" or subcommand == "E"):
                Option_C(subcommand)
      
            else:
                print("Not a valid command, try again please.")
        

def Option_C(command, user_input):

    response = " "

    if(command == "G"):
        
        while not (response == "M"):
            columns = input("Select columns to aggregate on:")
            # [columns...]
            print("Numeric column <column> requires bucketing. Enter buckets: <idk how to format this yet>")
            
            #   repeat above for all numeric columns]
            
            print("Distribution of videos according to above criteria:")
            #   [Spark output]
            response = input("\nMenu:\n [R]epeat\n [M]ain Menu\n")

            
    if(command == "R"):
        print("Export")
        while not (response == "S" or response == "A" ):
            
            response = input("Menu:\n [S]elected Columns\n  [A]ll Columns\n\n")
		     
            path = get_file("Input output directory:")
            print("Writing to ", path)
            
            if response == "S" :
                columns = input("Select columns:")
            
            elif response == "A":
                print("All columns")
                #[Spark stuff]

            else:
                print("Not a valid command, try again please.")
		        
    print("Finished...")
     
def main():
    #get_file("Enter input file(s) path:")
    menu_display()



def get_file(custom_text):
       
    file_exist = False
    while (file_exist == False):

        directory = input(custom_text)

        if os.path.isdir(directory):
            print("Reading Files...")
            file_exist = True
            return directory
            
        else:
            print(f"{directory} does not exist, please try again")
            



def menu_display(): 

    command = " "

    # repeat menu over and over until valid option is shown 
    while not (command == "E" ):
        print( "\n====Menu====\n [D]egree Distribution\n [C]ategorized Statistics\n [R]estart\n [E]xit\n\n")

        command = input("Enter Command:")
        
        # if command valid, go to option 
        if (command == "D" or command == "C" or command == "R"):
            menu_options(command)

        if (command == "E"):
            exit_variable = True

        # otherwise loop again 
        else:
            print("Not a valid command, try again please.")


if __name__ == "__main__":
    main()