import os
from degrees import write_degrees
from read import read_file
from stats import aggregate_columns
from avg_stats import write_avg_stats
from pyspark.sql.functions import concat_ws
from pyspark.sql import SparkSession

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
            "====Menu====\n [D]egree Distribution\n [C]ategorized Statistics\n [R]estart\n [S]ql Command\n [M]edian Stats for Categories\n [E]xit"
        )

        command = input("Enter Command: ")

        if command == "D":
            degree_distribution(df)
        elif command == "C":
            categorized_statistics(df)
        elif command == "R":
            df = input_file()
        elif command == "S":
            Full_SQL(df)
        elif command == "M":
            avg_category_stats(df)
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

def avg_category_stats(df):
    dir = input("Output directory: ")
    write_avg_stats(df, dir)
    print("Finished.")

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

def Full_SQL(df):
    
    #Start spark session 
    spark = SparkSession.builder.appName("MyApp").getOrCreate()
    
    # convert PySpark DataFrame to temporary table/view
    table_name = input("Enter table name: ")
    df.createOrReplaceTempView(table_name)

    # execute SQL command on the temporary table/view
    print("Use SQL commands ONLY, current table name is " + table_name)
    result = spark.sql(input())

    # show the result
    result.show()

    # get user to store file 
    while True: 
        print("Save these reults in CSV?")
        print("[N]o\n[Y]es\n")
        response = input("")
        if(response == "N"):
            print("Response not saved...")
            return
        if(response == "Y"):            
            output_dir = input("Enter output directory path: ")
            result.write.csv(output_dir, header=True)
            return
        else:
            print("Invalid input")

    #stop spark session 
    spark.stop()


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
