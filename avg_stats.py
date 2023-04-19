from pyspark.sql.functions import avg, expr, ceil, floor

def round_length_to_nearest_10(value):
    return ceil(value / 10) * 10

def round_views_to_nearest_100(value):
    return floor(value / 100) * 100

def write_avg_stats(df, dir):
    # Group the data by category
    grouped_df = df.groupBy('category')

    # Calculate the average video length and views for each category
    avg_length_expr = avg('length').alias('average_length')
    avg_views_expr = avg('views').alias('average_views')
    
    # Define median expressions and round them
    median_length_expr = round_length_to_nearest_10(expr('percentile_approx(length, 0.5)')).alias('median_length')
    median_views_expr = round_views_to_nearest_100(expr('percentile_approx(views, 0.5)')).alias('median_views')

    # Calculate the median and average video length and views for each category
    aggregated_df = grouped_df.agg(
        avg_length_expr,
        avg_views_expr,
        median_length_expr,
        median_views_expr
    )

    # Write the aggregated data as a CSV file to the specified directory
    aggregated_df.write.csv(dir, mode='overwrite', header=True)