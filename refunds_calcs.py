# Import section
import pandas as pd
import sys


# Function that gives you a dataframe based on the csv files of each asset

def get_df(symbol,path_to_folder):
    
    # Also, the stock information is contained into seperate files. We need to import and concatenate the info
        
        df1=pd.read_csv("{}/{}_1.csv".format(path_to_folder,symbol),\
                        usecols=[0,4]
                       )
        
        df2=pd.read_csv("{}/{}_2.csv".format(path_to_folder,symbol),\
                        usecols=[0,4]
                       )
        
        frames = [df2,df1]
        df = pd.concat(frames)
        
        # The time zone is not relevant to our assignment, and therefore we will only need format = "%Y-%m-%d"
        df["Date"] = df["Date"].apply(lambda row: row[:10])
        
        #Building a datetime index dataframe
        df = df.set_index('Date')
        df.index = pd.to_datetime(df.index,format = "%Y-%m-%d")
        
        return df    


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

    mapping = fund["Close"]

    users["Close_Price_Open"]=users["investment_open_date"].map(mapping)
    
    users["Close_Price_Close"]=users["investment_close_date"].map(mapping)
    
    
    
    # (investment_amount / close_price_on_opening_date) * close_price_on_refund_date
    
    users["amount_refund"] = (users["amount_invested"] / users["Close_Price_Open"]\
                              * users["Close_Price_Close"])


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
    
    # Creating the fund made out of the weighted average of each stock

    fund = pd.DataFrame()
    fund.index = facebook.index
    fund["Close"] = facebook["Close"]*0.15 + netflix["Close"]*0.1 + apple["Close"]*0.25 + \
                    tesla["Close"]*0.15 + google["Close"]*0.2 + amazon["Close"]*0.15
        
    
    # Uploading the users file into a pandas df
    users = read_users(path_to_folder)
        

    # Building a final pandas df with the new column amount_refunded

    output = calculate_amount_to_refund(users)
    
        
    # Saving the new df created as a csv file into the path_to_folder provided
    
    output.to_csv(path_to_folder + "/users_refund.csv", index=False)
