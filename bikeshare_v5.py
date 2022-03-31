import pandas as pd
import traceback
import sys


#create dictionary to to get dataset
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#function to load data:
def load_data(city, month, day):

    #===============================================================================
    #Loads data for the specified city and filters by month and day if applicable.
    #Args:
        #(str) city - name of the city to analyze
        #(str) month - name of the month to filter by, or "all" to apply no month filter
        #(str) day - name of the day of week to filter by, or "all" to apply no day filter
    #Returns:
        #df - pandas DataFrame containing city data filtered by month and day
    #==================================================================================
    # load data file into a dataframe
    try:

        df = pd.read_csv(CITY_DATA[city])

        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        #also concatenate start station and end station to create a new column
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour
        df['station_start_end'] = df['Start Station']+" "+df['End Station']


        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
    
            # filter by month to create the new dataframe
            df = df[df['month']==month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
    except Exception as e:
        print("Error reading "+city +" data for the month of"+month)
        traceback.print_exception(*sys.exc_info())
        print(str(e))
    return df


#Explore US BIKE share data:
print("hello there, lets explore some US BIKE share data: ")
#create a function that returns a dataframe of the filter:(git example)
def display_data():
    #Get inputs from the user:
    #city:
    print("choose city (chicago,new york city,washington)")
    city = input("Enter CITY: ").lower()
    #check the city entered and iterate until the correct city is input:
    while city not in ['chicago','new york city','washington']:
        print("Wrong city input. Enter one of: chicago,new york city,washington")
        city = input("Wrong city input. Enter the correct city: ")

    #month: filter by month.
    print("would you like to filter by month? Enter a month name(enter ''all'' for no filter): ")
    month = input('Enter Month: ').lower()

    #day of the week: Filter by day of the week.
    print("would you like to filter by day of the week? (Enter day_name or ''all'' for no filter )")
    day = input("Enter day of the week: ").capitalize()
    df_final = load_data(city,month,day)

    #Running basic statistics:
    print("running basic statistics on the data:")
    print("==============================================")
    print("1.) popupar times of travel: ")
    print("==============================================")
    common_month = df_final['month'].mode()[0]
    common_day_of_week = df_final['day_of_week'].mode()[0]
    common_hr_of_day = df_final['hour'].mode()[0]
    print("most common month: ",common_month)
    print("most common day of week: "+common_day_of_week)
    print("most common hour of day: ",common_hr_of_day)

    print("==============================================")
    print("2.) popupar stations and trip: ")
    print("==============================================")
    common_start_station = df_final['Start Station'].mode()[0]
    common_end_station = df_final['End Station'].mode()[0]
    common_start_end =  df_final['station_start_end'].mode()[0]
    print("common start station: "+common_start_station)
    print("common end station: "+common_end_station)
    print("common trip from start to end: "+common_start_end)

    print("==============================================")
    print("3.) Trip duration: ")
    print("==============================================")
    total_travel_time = df_final['Trip Duration'].sum()
    avg_travel_time = df_final['Trip Duration'].mean()
    print("total travel time: ",total_travel_time)
    print("average travel time: ",avg_travel_time)

    print("==============================================")
    print("4.) user information: ")
    print("==============================================")
    user_group_count = df_final['User Type'].value_counts()
    print("counts of each user type: ")
    print(user_group_count)
    if city != 'washington':
        count_gender = df_final['Gender'].value_counts()
        earliest_birth=df_final['Birth Year'].min()
        most_recent_birth = df_final['Birth Year'].max().astype('str')
        common_yr_of_birth = df_final['Birth Year'].mode()[0]
        print("earlies birth: ",earliest_birth)
        print("counts of each gender: ")
        print(count_gender)
        print("most recent birth: "+most_recent_birth)
        print("most common yr of birth: ",common_yr_of_birth)
    #function within a function(for sample data display) 
    print("create a function to display sample data") 
    def display_raw_data():
        try:
            print("Do you want to display sample data?")
            view_data = input("Do you want to display 5 rows of trip data?").lower()
            start_loc = 0
            while view_data != 'no':
                print(df_final.iloc[5])
                start_loc += 5
                view_data = input("Do you wish to continue?: ").lower()
        except Exception as e:
            print('Error reading data' )
            traceback.print_exception(*sys.exc_info())
            print(str(e))
    display_raw_data()

    print("END, successfully done statistics on the data and previewed sample records:")



def main():
   display_data()
if __name__ == '__main__':
    main()