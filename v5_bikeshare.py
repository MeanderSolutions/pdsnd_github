import time
import pandas as pd
import numpy as np
import datetime

#I wanted to learn how to support multiple input values.
#	For this purpose the code supports comma separated list of cities as an input.
#	Testing example can include cities outside of the CITY_DATA 
#	input: Moscow, Prague, Chicago - will properly recognise that we have data only for Chicago.
#	input: Moscow, Prague, Chicago, Washington - will properly recognise that we have data only for Chicago and Washington.

#I wanted to learn how to handle error in case of missing file.
#	In CITY_DATA I have added entry for Barcelona. 
#	If file barcelona.csv is not present - the error is handled properly.
#	Testing example can include Barcelona mixed with other cities.
#	input: Moscow, Prague, Barcelona, Chicago - will properly recognise that we have data only for Barcelona, Chicago.
#	                                          - will properly handle error in case barcelona.csv is missing	
#	                                          - will properly analyse data for Chicago 

#I also wanted to learn how to handle error for special case: 
#	when key columns are missing from the data file, that would crash load_data function
#	To demonstrate this functionality, I provided additional file barcelona.csv (uploaded with the project file)
#	If you have an option to add barcelona.csv to the existing .csv files in the project, please do so :)
#	If the file barcelona.csv is uploaded to the desired location, you can see error handling for the missing columns
#	columns deleted on puprose from barcelona.csv: [Start Date], [End Date], [Trip Duration] 


#CITY_DATA, months, days are global variables.
#This way all functions can use the data (if required).
#This also simulates that the values in these variables could be imported from external databases etc.

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
			  #'barcelona': 'barcelona.csv' 
			  }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
	"""
	The design of the function get_filters() allows users to chose more than one city for analysis.
	Asks user to specify a city/cities, month, and day to analyze.

	Returns:
		list of (str) cities  - names of the city/cities to analyze
		(str) month - name of the month to filter by, or "all" to apply no month filter
		(str) day - name of the day of week to filter by, or "all" to apply no day filter
	"""
	
	print('Hello! Let\'s explore some US bikeshare data!')
	
	###################
	## city / cities ##
	###################
    
	# get user input for city (chicago, new york city, washington). 
	while True:
		print('\nPlease enter the name of the city from the list')
		print('or comma separated names of the cities:\n')
		for key, value in CITY_DATA.items():
			print(key)
		print('\n')
		
		aninput = str(input('\t Your input: ')).lower()
		
		# # split input with the comma
		# alist=aninput.split(',')
		# # remove white spaces from the input
		# proper_list = [i.strip() for i in alist]
		# # remove empty elements from the input
		# final_list = list(filter(None, proper_list))
		
		# apply all three input clean-up steps in one line
		thelist = list(filter(None, [i.strip() for i in aninput.split(',')]))
		
		print('\nYou have entered: \n')
		for i in thelist:
			print(i.title())
			
		print('-'*40)
						
		# #get confirmation or give user a chance to correct input	
		# print('\nIs that correct? [yes] - proceed; [no] - correct the input\n')
		
		# while True:
			# testinput = input('\tPlease type [yes/no] :').lower()
			# if testinput == 'yes' or testinput == 'no':
				# break
		
		testinput = 'yes'
		if testinput == 'yes':
			
			#create empty list to store only the elements from user input that are present in our CITY_DATA dictionary
			cities = []
			
			#iterate thorugh user's input and append the list cities with correct input
			uniquelist = set(thelist)
			for city in uniquelist:
				if city in CITY_DATA:
					cities.append(city)
			
			#if CITY_DATA does not contain any of the entered names: 
			if not cities:
				print('-'*40)
				print('\nUnfortunately, we do not have data for the city/cities provided by you')
				print('Perhaps it is a typo or you did not separate the city names with comma\n\n')
				print('Please try again\n')
				print('-'*40)
				
			#if CITY_DATA contains all of some of the entered cities:
			else:
				print('-'*40)
				print('\nFrom the cities provided by you we have data for:\n')
				for i in cities:
					print(i.title())
				print('-'*40)
				#get confirmation from the user if he would like to analyse the data for the recognised cities
				print('\nWould you like to proceed to analysis? [yes] - proceed; [no] - input cities again\n')
				
				while True:
					testinput2 = input('\tPlease type [yes/no] :').lower()
					if testinput2 == 'yes' or testinput2 == 'no':
						break
				
				#check if we are ready to proceed to analysis
				if testinput2 == 'yes':
					break
	
	###########
	## month ##
	###########
	
	# get user input for month (all, january, february, ... , june)

	while True:
		print('-'*40)
		print('\nPlease enter the month from the list:\n {}\n To chose all months, please enter: all\n'.format(months))
		month = str(input('\t Your input: ')).lower()
		try:	
			if month != 'all':
			# use the index of the months list to get the corresponding int
				if month in months:
					num_month = months.index(month) + 1
					print('\nYou have chosen month: ', month.title())
					print('-'*40)
					break
				else:
					print('\nIt seems like you have entered the wrong month. Please try again\n')
					print('-'*40)
			elif month == 'all':
				print('\nYou have chosen all months from the list')
				print('-'*40)
				break
		except Exception as e:
			print('\nException occurred: {}. Try again!'.format(e))
			
			
	###########
	##  day  ##
	###########
	
	# get user input for day of week (all, monday, tuesday, ... sunday)

	while True:
		print('\nPlease enter the day from the list:\n {}\n To chose all days, please enter: all\n'.format(days))
		day = str(input('\t Your input: ')).lower()
		try:	
			if day != 'all':
			# use the index of the months list to get the corresponding int
				if day in days:
					num_day = days.index(day)
					print('\nYou have chosen day: ', day.title())
					print('-'*40)
					break
				else:
					print('\nIt seems like you have entered the wrong day. Please try again\n')
					print('-'*40)
					print('-'*40)
			elif day == 'all':
				print('\nYou have chosen all days from the list')
				print('-'*40)
				break
		except Exception as e:
			print('\nException occurred: {}. Try again!'.format(e))
			
    
	return cities, month, day
	

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
	
	#import sys
	
	filename = CITY_DATA[city]
	city_bikes = pd.read_csv(filename)

	#check if columns Start Time and End Time, required for analysis, are in dataframe
	start_time_in_df = 'Start Time' in city_bikes
	end_time_in_df = 'End Time' in city_bikes
	if start_time_in_df and end_time_in_df:
		#convert the Start Time and End Time column to datetime
		city_bikes['Start Time'] = pd.to_datetime(city_bikes['Start Time'])
		city_bikes['End Time'] = pd.to_datetime(city_bikes['End Time'])
			
		#extract month and day of week from Start Time to create new columns
		city_bikes['month'] = city_bikes['Start Time'].dt.month
		city_bikes['day_of_week'] = city_bikes['Start Time'].dt.dayofweek
		if month != 'all':
			num_month = months.index(month) + 1
			month_bikes = city_bikes[city_bikes['month'] == num_month]
		else:
			month_bikes = city_bikes
		
		if day != 'all':
			num_day = days.index(day)
			day_bikes = month_bikes[month_bikes['day_of_week'] == num_day]
		else:
			day_bikes = month_bikes
		return day_bikes
	#if the required columns are not present in dataframe, program will break
	else:
		print('It seems there is no [Start Time] and/or [End Time] columns in the data for the city {}.\n These columns are necessary to provide time analysis.'.format(city.title()))
		return city_bikes
		#sys.exit('Please start again')
		
	
print('-'*40)


def time_stats(city_bikes):
	"""Displays statistics on the most frequent times of travel."""
	
	#check if columns Start Time and End Time, required for analysis, are in dataframe
	start_time_in_df = 'Start Time' in city_bikes
	end_time_in_df = 'End Time' in city_bikes
	if start_time_in_df and end_time_in_df:
		
		print('\nCalculating The Most Frequent Times of Travel...\n')
		start_time = time.time()

		# display the most common month
		city_bikes['month'] = city_bikes['Start Time'].dt.month 
		most_common_month = city_bikes['month'].mode()[0]
		print('Most common month:', months[most_common_month-1].title())
		
		# display the most common day of week
		city_bikes['day_of_week'] = city_bikes['Start Time'].dt.dayofweek 
		most_common_day = city_bikes['day_of_week'].mode()[0]
		#print('Most common day of week:', most_common_day)
		print('Most common day of week:', days[most_common_day-1].title())

		# display the most common start hour
		city_bikes['hour'] = city_bikes['Start Time'].dt.hour 
		most_common_start_hour = city_bikes['hour'].mode()[0]
		print('Most common start hour:', most_common_start_hour, ' o\'clock')
		
		print("\nThis took %s seconds." % (time.time() - start_time))
	
	else:
		print('\n Skipping Travel Time analysis.\n')

print('-'*40)



def station_stats(city_bikes):
	"""Displays statistics on the most popular stations and trip."""

	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()
	
	start_station_in_df =  'Start Station' in city_bikes
	end_station_in_df = 'End Station' in city_bikes
	if start_station_in_df and end_station_in_df:
		# display most commonly used start station
		most_common_start_station = city_bikes['Start Station'].mode()[0]
		print('Most common start station: ', most_common_start_station)
		
		# display most commonly used end station
		most_common_end_station = city_bikes['End Station'].mode()[0]
		print('Most common end station: ', most_common_end_station)
		
		# display most frequent combination of start station and end station trip
		most_frequent_combination = city_bikes.groupby(['Start Station','End Station']).size().nlargest(1)
		print(type(most_frequent_combination))
		print('\nMost frequent combination of start station and end station trip:\n', most_frequent_combination)
	else:
		print('There is no data for start and end station for this particular city. \nWe cannot calculate the most popular station and trip')
	
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def trip_duration_stats(city_bikes):
	"""Displays statistics on the total and average trip duration."""

	print('\nCalculating Trip Duration...\n')
	start_time = time.time()
	
	trip_duration_in_df = 'Trip Duration' in city_bikes
	end_time_in_df = 'End Time' in city_bikes
	start_time_in_df =  'Start Time' in city_bikes
	if trip_duration_in_df:
		total_travel_time = city_bikes['Trip Duration'].sum()
		print('Total travel time: ', str(datetime.timedelta(seconds=int(total_travel_time))))
		# display mean travel time
		average_time = city_bikes['Trip Duration'].mean()
		print('Average time of the trip: ', str(datetime.timedelta(seconds=int(average_time))))
	else:
		if end_time_in_df and start_time_in_df:
			# display total travel time
			travel_time = (city_bikes['End Time'] - city_bikes['Start Time'])
			city_bikes['Travel Time'] = travel_time.dt.seconds 
			total_travel_time = city_bikes['Travel Time'].sum()
			print('Total travel time: ', str(datetime.timedelta(seconds=int(total_travel_time))))
			# display mean travel time
			average_time = city_bikes['Travel Time'].mean()
			print('Average time of the trip: ', str(datetime.timedelta(seconds=int(average_time))))
		else:
			print('Skipping trip duration stats - required data columns are missing')
	
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def user_stats(city_bikes):
	"""Displays statistics on bikeshare users."""

	print('\nCalculating User Stats...\n')
	start_time = time.time()

	# Display counts of user types
	usertype_count = city_bikes['User Type'].value_counts(dropna=False)
	print('User type:\n', usertype_count)
	# Display counts of gender
	gender_in_df = "Gender" in city_bikes
	if gender_in_df:
		gender_count = city_bikes['Gender'].value_counts(dropna=False)
		print('-'*20)
		print('Gender:\n', gender_count)
		city_bikes['Gender'] = False
	else: 
		print("There is no data about customers' gender for this particular city")
	print('-'*20)
	
	year_of_birth_in_df = 'Birth Year' in city_bikes
	if year_of_birth_in_df:
		# Display earliest year of birth
		earliest_year_of_birth = int(city_bikes['Birth Year'].min())
		print('The earliest year of birth: ', earliest_year_of_birth)
		#Display most recent year of birth
		most_recent_year_of_birth = int(city_bikes['Birth Year'].max())
		print('The most recent year of birth: ', most_recent_year_of_birth)
		#Display most common year of birth
		most_common_year_of_birth = int(city_bikes['Birth Year'].mode()[0])
		print('The most common year of birth: ', most_common_year_of_birth)
		city_bikes['Birth Year'] = False
	else:
		print("There is no data about customers' year of birth for this particular city")
	
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


	
def main():
	while True:
		cities, month, day = get_filters()
		for city in cities:
			print('-'*40)
			print('\nAnalysing data for city: {}\n'.format(city.title()))
			print('-'*40)
			df = load_data(city, month, day)
			time_stats(df)
			station_stats(df)
			trip_duration_stats(df)
			user_stats(df)
			print('\n')
		
		print('\nWould you like to restart? Enter yes or no.\n')
		while True:
			testinput = input('\tPlease type [yes/no] :').lower()
			if testinput == 'yes' or testinput == 'no':
				break
		if testinput != 'yes':
			break
		
if __name__ == "__main__":
	main()
			
			
			
			
			