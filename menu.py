import os

def main():
    # get_file("Enter input file(s) path:")
    menu()


def menu():
    # Read given file(s).
    df = input_file()

    # Display menu.
    command = " "
    while True:
        print(
            "====Menu====\n [D]egree Distribution\n [C]ategorized Statistics\n [R]estart\n [E]xit"
        )

        command = input("Enter Command:")

        if command == "D":
            degree_distribution()
        elif command == "C":
            categorized_statistics()
        elif command == "R":
            df = input_file()
        elif command == "E":
            break
        else:
            print("Not a valid command, please try again.")

def input_file():
    file = input("Enter input file(s): ")
    # Pass file data into Spark and return Dataframe.
    # Also return a second argument indicating success?
    return

def degree_distribution():
    dir = input("Output directory:")
    # Calculate degree stuff...
    print("Writing to ", dir, "...", sep="")
    # degrees.write.csv(...)
    # Don't need to return anything?
    print("Finished.")

def categorized_statistics():
    print("Filter data:")
    # Not sure what options I want yet
    # Just take a single SQL query to filter with?

    while True:
        command = input("[G]enerate statistics or [E]xport: ")
        if command == "G":
            generate_statistics()
            break
        elif command == "E":
            export()
            break
        else:
            print("Invalid input.")
    return

def generate_statistics():
    print("Select columns to aggregate on:")
    # Print columns, marking them if they have been selected already
    # Alternatively, just remove a column from the list if it has been selected

    # Get column choice
    column = input("> ")

    # If column is numeric
    print("Numeric column", column, "requires bucketing.")
    buckets = input("Enter buckets: ")

    # Save all selected columns/buckets in a list or something

    # Run Spark calculation

    print("Distribution of videos according to above criteria:")

    return 

def export():
    print("Export\n\t[S]elected Columns\n\t[A]ll Columns\n")
    command = input("> ")

    dir = input("Output directory:")
    print("Writing to ", dir, "...", sep="")
    # Spark stuff
    print("Finished.")
    return

if __name__ == "__main__":
    main()