from pyspark.ml.feature import Bucketizer

def aggregate_columns(df):
    df_columns = ["uploader", "age", "category", "length", "views", "rate", "ratings", "comments"]
    numeric_columns = ["age", "length", "views", "rate", "ratings", "comments"]

    print("Select columns to aggregate on:")
    df.printSchema()

    # Input is a space-separated list of column names
    # eg. age category length
    columns = input("> ").split()

    # Do not process the same column twice
    seen = []
    # Iterate over each column
    for column in columns:
        if column not in df_columns:
            print("Unrecognized column '", column, "'", sep="")
            continue

        # If the column has been seen before, ignore it
        if column in seen:
            continue

        # If the column is numeric, take in buckets
        if column in numeric_columns:
            print("Numeric column", column, "requires bucketing.")

            # eg. Enter buckets: 10 100 1000
            buckets = input("Enter buckets: ").split()

            # user should not input "inf"
            # technically the user can input "inf", needs decision
            buckets = [-float("inf")] + [float(i) for i in buckets] + [float("inf")] # cast to list of floats

            bucketizer = Bucketizer(splits=buckets, inputCol=column, outputCol=column+"_bucket")
            df = bucketizer.transform(df)

            # The bucket column needs to be used rather than the original column
            seen.append(column+"_bucket")
        else:
            # Otherwise, the column is a string column, which does not need to be bucketed
            seen.append(column)

    # Perform final groupBy
    print("Distribution of videos according to above criteria:")
    # Write to csv instead?
    df.groupBy(seen).count().sort("count", ascending=False).show()
    return