from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import array
from pyspark.sql.functions import array_contains
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
        .withColumn('backlinks', array()))

df = read_file('0222/1.txt')

df.show(1)

backlinks = df.select(df.videoID).where(array_contains(df.relatedIDs, 'LKh7zAJ4nwo')).show()
