import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # This is second changes for commit
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    valid_cities = ["chicago", "new york city", "washington"]  # Ensure the list is complete
    # Loop to get valid city input from the user
    while True:
        # Prompt the user for input
        city = input("Please input a city (e.g., Chicago, New York City, washington): ").strip().lower()   
        # Check if the input city is in the list of valid cities
        if city in valid_cities:
            # If valid, break out of the loop
            break     
        # If invalid, print an error message and prompt again
        print("Invalid city. Please enter a valid city from the list.")


    # get user input for month (all, january, february, ... , june)
    valid_month = ["all", "january", "february", "march", "april", "may", "june"]  # Ensure the list is complete
    # Loop to get valid month input from the user
    while True:
        # Prompt the user for input
        month = input("Please input a month (e.g., all, january, february, ... , june): ").strip().lower()   
        # Check if the input month is in the list of valid cities
        if month in valid_month:
            # If valid, break out of the loop
            break     
        # If invalid, print an error message and prompt again
        print("Invalid month. Please enter a valid month from the list.")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]  # Ensure the list is complete
    # Loop to get valid day of week input from the user
    while True:
        # Prompt the user for input
        day = input("Please input a day of week (e.g., all, monday, tuesday, ... sunday): ").strip().lower()   
        # Check if the input day of week is in the list of valid cities
        if day in valid_day:
            # If valid, break out of the loop
            break     
        # If invalid, print an error message and prompt again
        print("Invalid day. Please enter a valid day of week from the list.")


    print('-'*40)
    return city, month, day


def day_text_to_number(day_text):
    # Define a dictionary to map day names to numerical values
    day_to_number = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }
    # Convert the input to lowercase to handle case variations
    day_text = day_text.strip().lower()
    # Convert the day name to its numerical representation
    if day_text in day_to_number:
        return day_to_number[day_text]
    else:
        return None  # Return None for invalid day name


def month_text_to_number(month_text):
    # Define a dictionary to map month names to numerical values
    month_to_number = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6
    }

    # Convert the input to lowercase to handle case variations
    month_text = month_text.strip().lower()
    # Convert the month name to its numerical representation
    return month_to_number.get(month_text, None)  # Return None if month_text is not in the dictionary


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """# Validate city
    if city not in CITY_DATA:
        raise ValueError(f"City '{city}' not found in CITY_DATA.")
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Validate month and filter
    if month != "all":
        month_number = month_text_to_number(month)
        if month_number is None:
            raise ValueError(f"Invalid month: '{month}'")
        df = df[df['Start Time'].dt.month == month_number]

    # Validate day and filter
    if day != "all":
        day_number = day_text_to_number(day)
        if day_number is None:
            raise ValueError(f"Invalid day: '{day}'")
        df = df[df['Start Time'].dt.weekday == day_number]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    month_counts = df["Start Time"].dt.month.value_counts()
    most_common_month = month_counts.idxmax()
    print(f"The most common month is: {most_common_month}")

    # Display the most common day of the week
    day_counts = df["Start Time"].dt.dayofweek.value_counts()
    most_common_day = day_counts.idxmax()
    print(f"The most common day of the week is: {most_common_day}")

    # Display the most common start hour
    hour_counts = df["Start Time"].dt.hour.value_counts()
    most_common_hour = hour_counts.idxmax()
    print(f"The most common start hour is: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    if 'Start Station' in df.columns:
        most_common_start_station = df["Start Station"].value_counts().idxmax()
        print(f"The most commonly used start station is: {most_common_start_station}")
    else:
        print("Start Station column not found in the DataFrame.")

    # Display the most commonly used end station
    if 'End Station' in df.columns:
        most_common_end_station = df["End Station"].value_counts().idxmax()
        print(f"The most commonly used end station is: {most_common_end_station}")
    else:
        print("End Station column not found in the DataFrame.")

    # Display the most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        trip_combination = df.groupby(['Start Station', 'End Station']).size()
        most_common_trip = trip_combination.idxmax()
        print(f"The most frequent combination of start station and end station trip is: {most_common_trip}")
    else:
        print("Start Station or End Station column not found in the DataFrame.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Check if 'Trip Duration' column exists in the DataFrame
    if 'Trip Duration' in df.columns:
        # Ensure 'Trip Duration' is numeric
        df['Trip Duration'] = pd.to_numeric(df['Trip Duration'], errors='coerce')
        
        # Calculate total travel time
        total_travel_time = df['Trip Duration'].sum()
        print(f"Total travel time: {total_travel_time:.2f} seconds")

        # Calculate mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print(f"Mean travel time: {mean_travel_time:.2f} seconds")
    else:
        print("The 'Trip Duration' column is not found in the DataFrame.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Check and display counts of user types
    if 'User Type' in df.columns:
        user_type_counts = df['User Type'].value_counts().reset_index(name='Count')
        user_type_counts.columns = ['User Type', 'Count']
        print("Counts of user types:")
        print(user_type_counts)
    else:
        print("The 'User Type' column is not found in the DataFrame.")

    # Conditional statistics for cities other than Washington
    if city.lower() != "washington":
        # Check and display counts of gender
        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts().reset_index(name='Count')
            gender_counts.columns = ['Gender', 'Count']
            print("Counts of gender:")
            print(gender_counts)
        else:
            print("The 'Gender' column is not found in the DataFrame.")

        # Check and display statistics related to birth year
        if 'Birth Year' in df.columns:
            df['Birth Year'] = pd.to_numeric(df['Birth Year'], errors='coerce')

            # Display earliest, most recent, and most common year of birth
            earliest_birth_year = df['Birth Year'].min()
            most_recent_birth_year = df['Birth Year'].max()
            most_common_birth_year = df['Birth Year'].mode()

            print(f"Earliest year of birth: {earliest_birth_year:.0f}")
            print(f"Most recent year of birth: {most_recent_birth_year:.0f}")

            if not most_common_birth_year.empty:
                print(f"Most common year of birth: {most_common_birth_year.iloc[0]:.0f}")
            else:
                print("No common year of birth data available.")
        else:
            print("The 'Birth Year' column is not found in the DataFrame.")

    print("\nThis took %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays chunks of data from the DataFrame based on user input."""
    
    start_loc = 0
    while start_loc < len(df):
        user_input = input("\nWould you like to view 5 rows of individual trip data? Enter 'yes' or 'no': ").strip().lower()
        
        if user_input == 'yes':
            # Display the next 5 rows of data
            chunk = df.iloc[start_loc:start_loc + 5]
            print(chunk)
            start_loc += 5
            
            # Check if there are more rows to display
            if start_loc >= len(df):
                print("\nNo more data to display.")
                break
        elif user_input == 'no':
            print("\nExiting data display.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
