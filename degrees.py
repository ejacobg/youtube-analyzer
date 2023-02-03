from read import read_file
from pyspark.sql.functions import count, explode

# Drop bad values before continuing.
df = read_file(['./0222/*.txt']).dropna()

#show 
df.show(1)

related = df.select(df.videoID, explode(df.relatedIDs).alias('relatedID'))
# related.show()

backlinks = related.groupBy('relatedID').agg(count('videoID').alias('backlinks')).withColumnRenamed('relatedID', 'videoID')

# backlinks.sort('backlinks', ascending=False).show()

# Some videos do not have any backlinks, and thus their value is `null`. Change this to 0 to avoid problems when calculating the degree.
degrees = df.join(backlinks, df.videoID == backlinks.videoID, 'leftouter').select(df.videoID, 'links', 'backlinks').fillna(0)
degrees = degrees.withColumn('degree', degrees.links + degrees.backlinks)
degrees.sort('degree').write.csv('degrees', mode='overwrite', header=True)