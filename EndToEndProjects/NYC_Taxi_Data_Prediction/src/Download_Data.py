import argparse
import wget
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", type=int, default=2009, help="Start year for data download")
    parser.add_argument("--end_year", type=int, default=2019, help="Start year for data download")
    parser.add_argument("--output_dir", type=str, default=f'{os.getcwd()}/EndToEndProjects/NYC_Taxi_Data_Prediction/', help="Start year for data download")

    start_year, end_year = args.start_year, args.end_year
    start_year, end_year = 2019, 2019
    out_dir = f'{os.getcwd()}/EndToEndProjects/NYC_Taxi_Data_Prediction/'
    #start_month = 1, end_month = 12

    link_format = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{}-{}.parquet"

    for year in range( + 1):
        for month in range(1, 13):
            month_str = f"{month:02d}"
            link = link_format.format(year, month_str)
            print(link)
            print(f"Downloading data from {link}")
            # Following is not able to download the file
            wget.download(link)