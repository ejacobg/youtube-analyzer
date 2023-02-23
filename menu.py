import os
from degrees import write_degrees
from read import read_file
from stats import aggregate_columns
from pyspark.sql.functions import concat_ws

def main():
    # get_file("Enter input file(s) path:")
    #setLogLevel("ERROR")
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

        command = input("Enter Command: ")

        if command == "D":
            degree_distribution(df)
        elif command == "C":
            categorized_statistics(df)
        elif command == "R":
            df = input_file()
        elif command == "E":
            break
        else:
            print("Not a valid command, please try again.")


def input_file():
    # List multiple files as a space-separated list. 
    file = input("Enter input file(s): ").split()
    # Pass file data into Spark and return Dataframe.
    # Also return a second argument indicating success?
    return read_file(file).dropna()


def degree_distribution(df):
    dir = input("Output directory: ")
    write_degrees(df, dir)
    print("Finished.")



def categorized_statistics_gui(df, condition):
    # Not sure what happens if filter is empty
    # Use case is supposed to be for queries like "generate statistics for views > 10000"
    if condition != "":
        df = df.filter(condition)
        df.show()

    while True:
        command = input("[G]enerate statistics or [E]xport: ")
        if command == "G":
            generate_statistics(df)
            break
        elif command == "E":
            export(df)
            break
        else:
            print("Invalid input.")
    return


def categorized_statistics(df):
    # Not sure what happens if filter is empty
    # Use case is supposed to be for queries like "generate statistics for views > 10000"
    condition = input("Filter data: ")
    if condition != "":
        df = df.filter(condition)
        df.show()

    while True:
        command = input("[G]enerate statistics or [E]xport: ")
        if command == "G":
            generate_statistics(df)
            break
        elif command == "E":
            export(df)
            break
        else:
            print("Invalid input.")
    return


def generate_statistics(df):
    aggregate_columns(df)
    return


def export(df):
    print("Export\n\t[S]elected Columns\n\t[A]ll Columns\n")

    columns = df.columns
    while True:
        command = input("> ")
        if command == "S":
            df.printSchema()
            # Space-separated list (won't be checking duplicates)
            columns = input("Enter columns: ").split()
            break
        elif command == "A":
            break
        else:
            print("Invalid input.")

    dir = input("Output directory: ")
    print("Writing to ", dir, "...", sep="")

    if "relatedIDs" in columns:
        # relatedIDs must be the last item in the csv since it is a list
        columns.remove("relatedIDs")
        columns.append("relatedIDs")
        
        copy = df.withColumn("relatedIDs", concat_ws(",", "relatedIDs"))
    else:
        copy = df

    # Spark stuff
    copy.select(columns).write.csv(dir, mode="overwrite", header=True)
    print("Finished.")
    return


if __name__ == "__main__":
    main()
