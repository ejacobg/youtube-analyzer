from pyspark.ml.feature import Bucketizer

def aggregate_columns(df):
    df_columns = ["uploader", "age", "category", "length", "views", "rate", "ratings", "comments"]
    numeric_columns = ["age", "length", "views", "rate", "ratings", "comments"]

    print("Select columns to aggregate on:")
    df.printSchema()

    # Input is a space-separated list of column names
    # eg. age category length
    columns = input("> ").split()

    # Iterate over each column
    for column in columns:
        if column not in df_columns:
            print("Unrecognized column '", column, "'", sep="")
            continue
        # If the column is numeric, take in buckets
        if column in numeric_columns:
            print("Numeric column", column, "requires bucketing.")

            # eg. Enter buckets: 10 100 1000
            buckets = input("Enter buckets: ").split()

            # user should not input "inf"
            buckets = [-float("inf")] + [float(i) for i in buckets] + [float("inf")] # cast to list of floats

            bucketizer = Bucketizer(splits=buckets, inputCol=column, outputCol=column+"_bucket")
            df = bucketizer.transform(df)
        
        # technically nothing else needs to be done if the column is of type string


    # Perform final groupBy
    print("Distribution of videos according to above criteria:")
    # Invalid columns need to be removed before being passed in
    # df.groupBy(columns).count()
    return