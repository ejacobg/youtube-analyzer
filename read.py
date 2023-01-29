from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import array, array_contains, count, explode, size
from pyspark.sql.types import *

sc = SparkContext('local')
spark = SparkSession(sc)

def read_file(file):
    df = spark.read.csv(file, sep='\t')

    df = df.select(*df.columns[:9], array(df.columns[9:])).toDF('videoID', 'uploader', 'age', 'category', 'length', 'views', 'rate', 'ratings', 'comments', 'relatedIDs')

    return (df.withColumn('age', df.age.cast('int'))
        .withColumn('length', df.length.cast('int'))
        .withColumn('views', df.views.cast('int'))
        .withColumn('rate', df.rate.cast('float'))
        .withColumn('ratings', df.ratings.cast('int'))
        .withColumn('comments', df.comments.cast('int'))
        .withColumn('links', size('relatedIDs')))

df = read_file(['./0222/0.txt', './0222/1.txt'])

df.show(1)

related = df.select(df.videoID, explode(df.relatedIDs).alias('relatedID'))
# related.show()

backlinks = related.groupBy('relatedID').agg(count('videoID').alias('backlinks')).withColumnRenamed('relatedID', 'videoID')

# backlinks.sort('backlinks', ascending=False).show()

degrees = df.join(backlinks, df.videoID == backlinks.videoID, 'leftouter').select(df.videoID, 'links', 'backlinks')
degrees = degrees.withColumn('degree', degrees.links + degrees.backlinks)
degrees.sort('degree', ascending=False).show()