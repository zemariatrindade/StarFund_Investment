# Import section
import pandas as pd
import sys


# Function that builds a dataframe based on the csv files of each asset in the folder

def get_df(symbol,path_to_folder):
    
    # I'll drop the last column stock splits as it only contains null values and it's not relevant to this assignment
    # Also, the stock information is contained into seperate files. We need to import and concatenate the info
        
        df1=pd.read_csv("{}/{}_1.csv".format(path_to_folder,symbol),\
                        usecols=[0,1,2,3,4,5,6]
                       )
        
        df2=pd.read_csv("{}/{}_2.csv".format(path_to_folder,symbol),\
                        usecols=[0,1,2,3,4,5,6]
                       )
        
        frames = [df2,df1]
        df = pd.concat(frames)
        
        # The time zone is not relevant to our assignment, and therefore we will only need format = "%Y-%m-%d"
        df["Date"] = df["Date"].apply(lambda row: row[:10])
        
        #Building a datetime index
        df = df.set_index('Date')
        df.index = pd.to_datetime(df.index,format = "%Y-%m-%d")
        
        return df 


# Function that builds a pandas series with a cumulative performance of a given stock

def daily_performance(df):
    
    #Creating a new column called Performance that is the grow rate of the close price between 2 business consecutive days
    
    df["Performance on close"] = ((df["Close"]/df["Close"].shift(1))-1)*100
    df[df.index == "2022-12-01"] = 0
    
    # Getting the cumulative of performance
    df["Cumulative Performance on close"] = df["Performance on close"].cumsum()
    
    return df["Cumulative Performance on close"]



# For reading the users.csv
decimal_separator = "."
thousands_separator = ""
date_format = "%Y/%m/%d"


# Function that reads the csv file and returns a df

def read_users(path_to_folder):
    
    users = pd.read_csv(filepath_or_buffer = path_to_folder + "/users.csv",\
               parse_dates=["investment_open_date","investment_close_date"],\
               date_format = date_format,\
               decimal=decimal_separator,\
               #thousands=thousands_separator
               )
        
    return users



# Function that adds the amount_refund column with map, and returns the final df


def calculate_amount_to_refund(users):

    mapping = table["Fund Cumulative Performance on close"]
    users["cumulated performance on open"]=users["investment_open_date"].map(mapping)
    
    users["cumulated performance on close"]=users["investment_close_date"].map(mapping)
    
    users["amount_refund"] = (users["amount_invested"] * \
                              (1 + users["cumulated performance on close"]/100\
                               - users["cumulated performance on open"]/100))#.round(2) 


    # Slicing our df for the relevant columns
    output = users[["user_id","investment_open_date","investment_close_date",\
                    "amount_invested","amount_refund"]]
        
    return output


if __name__ == '__main__':
    
    path_to_folder = sys.argv[1]
    
    # Getting a df for every asset of our study
    
    facebook = get_df('META',path_to_folder)
    netflix = get_df('NFLX',path_to_folder)
    apple = get_df('AAPL',path_to_folder)
    tesla = get_df('TSLA',path_to_folder)
    google = get_df('GOOGL',path_to_folder)
    amazon = get_df('AMZN',path_to_folder)
    
    
    table = pd.DataFrame()
    table["facebook"] = daily_performance(facebook)
    table["netflix"] = daily_performance(netflix)
    table["apple"] = daily_performance(apple)
    table["tesla"] = daily_performance(tesla)
    table["google"] = daily_performance(google)
    table["amazon"] = daily_performance(amazon)
    
    # New column for the fund which is a combination of the previous ones
    table["Fund Cumulative Performance on close"] = table["facebook"]*0.15 + table["netflix"]*0.1\
                                + table["apple"]*0.25 + table["tesla"]*0.15\
                                + table["google"]*0.20 + table["amazon"]*0.15
    
    table = table[["Fund Cumulative Performance on close"]]
    
    
    # Uploading the users file into a pandas df
    users = read_users(path_to_folder)
        

    # Building a final pandas df with the new column amount_refunded

    output = calculate_amount_to_refund(users)
    
        
    # Saving the new df created as a csv file into the path_to_folder provided
    
    output.to_csv(path_to_folder + "/users_refund.csv", index=False)
    
