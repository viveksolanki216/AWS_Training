
# NYC Taxi Prediction


### Download the data. 
- Manually download the dataset from the [NYC gov link](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
- Or write a script as "Download_Data.py", but it's not working.

Data will be in different parquet files at month level.

#### Parquet files
- columnar storage format, i.e. you can read only the columns you need.
- Binary format (Non-readable)
- efficient, fast, takes less memory for large datasets.

#### How to quickly explore the data?
When data is large and couldn't fit in memory i.e. pandas dataframe, we can use:
##### **AWS Athena**: Serverless query service to analyze data in S3 using SQL.

How Athena Works with S3: Athena lets you run SQL queries directly on S3 files in formats like: CSV, JSON, Parquet (columnar + compressed, best performance),  ORC, Avro, Gzipped data

It’s completely serverless, so You don’t provision infrastructure You pay per query, per amount of data scanned

How to Use Athena on S3 Files (Steps)
1. Create a Glue Crawler (Once): 
    - A Glue Crawler is a tool that automatically scans your raw data in S3 (or other sources), detects the schema, and creates a table in the Glue Data Catalog. 
    - Scans multiple files and creates a single table if they have the same schema.
    - It doesn't create the table in a traditional database, but the metadata/schema is stored in the Glue Data Catalog, which Athena can query. Like a pointer to the s3 data.
    - Might need to update schema, as Glue Crawler might not detect all columns correctly, especially if the data is in multiple files.

    To automatically detect schema and create a queryable table:
    
    Go to AWS Glue > Crawlers

    Set S3 path to:
    s3://nyc-tlc/trip-data/
    
    Glue will scan the 24 .parquet files and extract the schema
    
    🎯 Output: A table like yellow_tripdata under a Glue database, ready for Athena

   There will be a Glue Service Role created automatically, which has permissions to read from S3 and write to the Glue Data Catalog. Add following permissions to the role:
   - AWSGlueConsoleFullAccess
   - CloudWatchLogsFullAccess

   2. Query via Athena
   Go to Athena > Query Editor, and:

    `SELECT * FROM yellow_tripdata WHERE tpep_pickup_datetime BETWEEN DATE '2023-01-01' AND DATE '2023-01-31' LIMIT 10;`

   2. Without Glue (Advanced Option)
   You can create the table manually:

    ` CREATE EXTERNAL TABLE yellow_tripdata (
      VendorID int,
      tpep_pickup_datetime timestamp,
      tpep_dropoff_datetime timestamp,
      passenger_count int,
      trip_distance double,
      ...
    )
    STORED AS PARQUET
    LOCATION 's3://nyc-tlc/trip-data/';`

    But using a Glue Crawler is easier and avoids schema mistakes.
    
    


