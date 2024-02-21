import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    
    city = input("Which city`s bikeshare data you want to explore, chicago, new york city or washington?  \n").lower()
   
    while city.lower() not in CITY_DATA:
        city = input("Please enter one of city name; chicago, new york city, washington. \n").lower()


    # Get user input for month (all, january, february, ... , june).

    month = input("Please enter a name of month you want to explore: all, january, february, march, april, may, june \n").lower()
    
    while month.lower() not in MONTH_DATA:
        month= input("Please enter a valid month name. \n").lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday).
   
    day = input("Please enter a day name: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday \n").lower()
    
    while day.lower() not in DAY_DATA:
        day= input("Invalid day name, please enter a day name. \n").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data as csv.
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datatime type.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day from the Start Time column to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Here we fillter data by month or apply all.
    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        
        month = MONTH_DATA.index(month)
        df = df[df['month'] == month]

    # Here we filter data by day of week or apply all.
    if day !=  'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    most_common_month = df['month'].mode()[0]
    print("Most common month from filter is: " + MONTH_DATA[most_common_month].title())

    # Display the most common day of week.

    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("Most common day of week from your filter is: " , most_common_day_of_week)

    # Display the most common start hour.
    most_common_start_hour = df['hour'].mode()[0]
    print("Most common start hour is: " , str(most_common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is: ', start_station, '\n')

    # Display most commonly used end station.
    end_station = df['End Station'].mode()[0]

    print('Most commonly used end station is: ', end_station, '\n')

    # Display most frequent combination of start station and end station trip.
    df['start_end_combination'] = df.apply(lambda x:'%s - %s' % (x['Start Station'],x['End Station']),axis=1)

    combination=df['start_end_combination'].mode()[0]

    print('Most frequent combination of start station and end station trip is: ',combination, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel = df['Trip Duration'].sum()
    print('\nTotal travel time : ' + str(total_travel))

    # Display mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print("Avarage of travel duration : " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    This function gives information about the user type, gender and birth year
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_type_total = df['User Type'].value_counts()
    print('Count of user type is : ' + str(user_type_total), '\n')

    # Display counts of gender.
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Total counts of gender : ', gender_count, "\n")

    # Display year of birth.
    if 'Birth Year' in df.columns:

        # Display earliest year of birth.
        earliest_year = df['Birth Year'].min()
        print('Earliest birth year : ', earliest_year , '\n')
        # Display most recent year of birth.
        recent_year = df['Birth Year'].max()
        print('Recent birth year : ',recent_year, '\n')
        # Display most common year of birth.
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('Most common of birth year : ', most_common_year, '\n' )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
def view_raw_data(df):
    """ Ask user if they want to see raw data.
        This function will bring data from csv file. 
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day.
    """

    i = 1
    
    while True:
        raw_data=input('Would you like to view 5 lines of raw data? Enter Yes or No. \n')
        if raw_data.lower() == 'yes':
            print(df[i:i+5])
            i +=5
        elif raw_data.lower() == 'no':
            break
        else:
            print('invalid command. \n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
