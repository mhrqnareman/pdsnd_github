import time
import pandas as pd

# Mapping of city names to csv filenames
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    def get_valid_input(prompt, valid_options):
    """
    Repeatedly prompt user until they enter a valid option.
    """
    while True:
        response = input(prompt).lower()
        if response in valid_options:
            return response
        else:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_valid_input('Would you like to see data for Chicago, New York City, or Washington?\n', CITY_DATA.keys())

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = get_valid_input('Which month? January, February, March, April, May, June, or "all"?\n', months)

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = get_valid_input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or "all"?\n', days)

    print('-'*40)
    return city, month, day
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df
def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    index = 0
    while True:
        show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").lower()
        if show_data != 'yes':
            break
        if index >= len(df):
            print("No more data to show.")
            break
        print(df.iloc[index:index+5])
        index += 5
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', most_common_month)

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', most_common_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', start_station)

    # Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', end_station)

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print('Most Common Trip from Start to End:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time, "seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', mean_travel_time, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender_counts)
    else:
        print('\nGender data not available for this city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])

        print('\nEarliest Birth Year:', earliest_year)
        print('Most Recent Birth Year:', most_recent_year)
        print('Most Common Birth Year:', most_common_year)
    else:
        print('\nBirth Year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """
    Runs the interactive bikeshare data exploration program.
    
    This function:
    - Prompts the user for city, month, and day filters.
    - Loads the corresponding data.
    - Displays statistics and raw data upon request.
    - Repeats the process until the user chooses to exit.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
    