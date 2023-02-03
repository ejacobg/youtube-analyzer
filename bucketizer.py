from pyspark.ml.feature import Bucketizer
from pyspark.sql.functions import max, min
from read import read_file

# Why are there null values? Are there some improperly-formatted data?
# Yes, there are some bad data: My531wSgReM, r_0LhWpZJaA, etc.
# Basically just look at the data files and see where there are gaps. Each row should have at least 9 items.
# Alternatively, just drop these bad data (use .dropna()).
df = read_file(['./0222/*.txt']).dropna()

# Count number of bad rows. Confirm with this regex: ^.{11}\r\n
# print(df.select('*').where('views is null').count())

buckets = [-float('inf'), 10, 100, 1000, 10000, 1000000, float('inf')]

bucketizer = Bucketizer(splits=buckets, inputCol='views', outputCol='bucket')

df = bucketizer.transform(df)

df.agg(max('views')).show()

df.groupBy('bucket').count().sort('bucket').show()