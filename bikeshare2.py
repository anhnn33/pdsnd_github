import time
import pandas as pd
import numpy as np
import calendar
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_input(prompt, options):
    """
    Asks user to specify an option from a list of options.

    Args:
        prompt (str): The prompt message to display to the user.
        options (list): The list of valid options.

    Returns:
        (str) user_input - The user's input that matches one of the options.
    """
    user_input = ''
    while user_input not in options:
        user_input = input(prompt).lower()
    return user_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington)
    cities = ['chicago', 'new york city', 'washington']
    city = get_input('Input city (chicago, new york city, washington): ', cities)

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    month = get_input('Input month: ', months)
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = get_input('Input day of week: ', days)

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['Day'] == day.title()]   
    df['Hour'] = df['Start Time'].dt.hour
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    cammon_month = df['Month'].mode()[0]
    print(cammon_month)
    # TO DO: display the most common day of week
    cammon_day = df['Day'].mode()[0]
    print(cammon_day)
    # TO DO: display the most common start hour
    cammon_hour = df['Hour'].mode()[0]
    print(cammon_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Travel map'] = df['Start Station'] + ' => '+ df['End Station']
    common_travel_map = df['Travel map'].mode()[0]
    print('Most frequent combination of start station and end station trip: ', common_travel_map)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    # TO DO: display total travel time
    print('Total travel time: ', total_travel_time)
    
    mean_travel_time = df['Trip Duration'].mean()
    # TO DO: display mean travel time
    print('Mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_type_counts = df['User Type'].value_counts()
    # TO DO: Display counts of user types
    print('Count of user types: ', user_type_counts)
    
    try:
        gender_counts = df['Gender'].value_counts()
        # TO DO: Display counts of gender
        print('Count of gender: ', gender_counts)
    except:
        # Skip if cant find the gender
        print('No Gender data availbale for your city')
    try:
        earliest_year_birth = int(df['Birth Year'].min())
        recent_year_birth = int(df['Birth Year'].max())
        cammon_year_birth = int(df['Birth Year'].mode()[0])
    
        # TO DO: Display earliest, most recent, and most common year of birth
        print('Earliest year of birth: ', earliest_year_birth)
        print('Recent year of birth: ', recent_year_birth)
        print('Cammon year of birth: ', cammon_year_birth)
    except:
        # Skip if cant find the birth         
        print('No Birth data availbale for your city')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Display 5 rows data when user press"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        start_loc += 5
        print(df.head(start_loc))
        view_data = input("Do you wish to continue?: ").lower()
        
def main():
    get_filters()
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
 
