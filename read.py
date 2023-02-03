from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import array, size
from pyspark.sql.types import *

sc = SparkContext('local')
spark = SparkSession(sc)

def read_file(file):
    #read data between the columns 
    df = spark.read.csv(file, sep='\t')
    
    #renamed columns
    df = df.select(*df.columns[:9], array(df.columns[9:])).toDF('videoID', 'uploader', 'age', 'category', 'length', 'views', 'rate', 'ratings', 'comments', 'relatedIDs')

    #read data of each columns as string and cast them to right datatype 
    return (df.withColumn('age', df.age.cast('int'))
        .withColumn('length', df.length.cast('int'))
        .withColumn('views', df.views.cast('int'))
        .withColumn('rate', df.rate.cast('float'))
        .withColumn('ratings', df.ratings.cast('int'))
        .withColumn('comments', df.comments.cast('int'))
        .withColumn('links', size('relatedIDs')))

