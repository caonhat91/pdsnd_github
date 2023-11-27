import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def verifyInput(msg, ans):
    inp = ''
    while True:
        print("\n" + msg + "\n")
        # in here, i handled the input,
        # both washington and WasHingTON should be accepted
        inp = input().lower()
        if inp in ans:
            break
        else:
            print("Sorry, i don't understand.\n")
            print(f"You must input {ans}.\n")

    return inp


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
                        or "all" to apply no month filter
                        and "all" must be default
        (str) day - name of the day of week to filter by,
                        or "all" to apply no day filter
                        and "all" must be default
    """
    print('-'*40)
    print('\n\n\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = verifyInput(
        "Would you like to see data for Chicago, New York, or Washington?",
        list(CITY_DATA.keys())
    )

    choosed = verifyInput(
        """Would you like to filter the data by month, day, or not at all?
Type 'none' for no time filter.""",
        ['month', 'day', 'none']
    )

    month = 'all'
    day = 'all'

    # get user input for month (all, january, february, ... , june)
    if ('month' == choosed):
        month = verifyInput(
            """Which month - Jan, Feb, Mar, Apr, May, or Jun?
Type 'all' to apply no month filter.""",
            ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
        )

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if ('day' == choosed):
        day = verifyInput(
            """Which day - Monday, Tuesday, Wednesday,
Thursday, Friday, Saturday, or Sunday?
Type 'all' to apply no day filter.""",
            ['all', 'monday', 'tuesday', 'wednesday',
             'thursday', 'friday', 'saturday', 'sunday']
        )

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day
    if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
                        to apply no month filter
        (str) day - name of the day of week to filter by, or "all"
                        to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered
                        by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the Start Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Day Of Week:', popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_fre_comb = (df['Start Station'] + "~" + df['End Station'])
    popular_fre_comb = popular_fre_comb.mode()[0]
    print('Most frequent combination of start station and end station trip:',
          ' -> '.join(popular_fre_comb.split("~")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Average travel time :", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        df (DataFrame): DataFrame of csv file
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print("Counts Of User Type:", *count_user_types, sep="\n")

    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
    except Exception:
        count_gender = [""]
    finally:
        print("Counts Of Gender:", *count_gender, sep="\n")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
    except Exception:
        earliest = ""
        most_recent = ""
        most_common = ""
    finally:
        print("Earliest Year Of Birth:", earliest)
        print("Most Recent Year Of Birth:", most_recent)
        print("Most Common Year Of Birth:", most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df, row=5):
    """Display raw data upon request by user

    Args:
        df (DataFrame): DataFrame of csv file
        row (int, optional): Row display. Defaults to 5.
    """

    # Display header of CSV file
    print(df.head())

    # Display 5 row of raw data
    next = 0
    while True:
        choosed = verifyInput(
            """Would you like to see 5 lines of raw data?
Type 'yes'/'no' for display.""",
            ['yes', 'no']
        )
        if ('yes' != choosed):
            return
        print(df.iloc[next:next + row])
        next += row


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if (df.shape[0] == 0):
            print("\nData is empty.\n")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

        restart = verifyInput(
            'Would you like to restart? Enter yes or no.', ['yes', 'no']
        )
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
