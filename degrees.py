from read import read_file
from pyspark.sql.functions import count, explode

# Drop bad values before continuing.
# df = read_file(['./0222/*.txt']).dropna()
# df.show(1)


def write_degrees(df, dir):
    related = df.select(df.videoID, explode(df.relatedIDs).alias('relatedID'))
    # related.show()

    backlinks = related.groupBy('relatedID').agg(count('videoID').alias('backlinks')).withColumnRenamed('relatedID', 'videoID')

    # backlinks.sort('backlinks', ascending=False).show()

    # Some videos do not have any backlinks, and thus their value is `null`. Change this to 0 to avoid problems when calculating the degree.
    degrees = df.join(backlinks, df.videoID == backlinks.videoID, 'leftouter').select(df.videoID, 'links', 'backlinks').fillna(0)
    degrees = degrees.withColumn('degree', degrees.links + degrees.backlinks)

    print("Writing to ", dir, "...", sep="")
    degrees.sort('degree').write.csv(dir, mode='overwrite', header=True)
    return
