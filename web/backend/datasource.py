import psycopg2
import getpass
import datetime
import numpy as np
from datetime import timedelta

class DataSource:
	'''
	DataSource executes all of the queries on the database.
	It also formats the data to send back to the frontend, typically in a list
	or some other collection or object.
	'''

	def __init__(self,user,password):
			'''
			Initializes the connection to the database.
			PARAMETERS
				user - the username, which is also the name of the database
				password - the database password
			'''
			try:
				# NOTE: include host="localhost" if the database is NOT in your home directory
				self.connection = psycopg2.connect(database=user, user=user, password=password, host="localhost")
			except Exception as e:
				print("Connection error: ", e)
				exit()


	def getCasesOnState(self, state):
			'''
			Returns the number of accumulated COVID-19 cases from the specified state on the particular day.
			PARAMETERS:
				state
				date (default: last updated day)
			RETURN:
				the number of accumulated COVID-19 cases from the specified state on the particular day.
			'''

			lastUpdate = "'2020-05-04 20:00:00'"
			try:
				cursor = self.connection.cursor()
				query = "SELECT confirmed FROM alldatausa WHERE place =" +"'" + state +"' and date = "+ lastUpdate +";"
				cursor.execute(query)
				return cursor.fetchall()
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None


	def getCasesByType(self, casetype, date='2020-05-04 20:00:00'):
			'''
			Returns the number of accumulated COVID-19 cases by its type.
			PARAMETERS:
				type - active, recovered, death
				date - (default: last updated day)
			RETURN:
				the number of accumulated COVID-19 cases by its type
			'''

			try:
				cursor = self.connection.cursor()
				query = "SELECT place, " + casetype + " FROM alldatausa WHERE date = '" + date + "';"
				cursor.execute(query)
				return cursor.fetchall()
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None


	def getCasesInDateRange(self, start, end):
			'''
			Returns the accumulated number of COVID-19 cases in the specified date range.
			PARAMETERS:
				start - the starting date of the range
				end - the ending date of the range
			RETURN:
				the accumulated number of COVID-19 cases in the specified date range
			'''

			try:
				cursor =self.connection.cursor()
				query = "SELECT place, date, confirmed FROM alldatausa WHERE date between '" + start + "' AND '" + end + "';"
				cursor.execute(query)
				result_list=cursor.fetchall()
				date_set = []
				state_list = []
				case_list = []
				i = 0
				while i < len(result_list):
					row = result_list[i]
					state = row[0]
					state_list.append(state)
					date = row[1]
					date_set.append(date)
					num_cases = row[2]
					case_list.append(num_cases)
					i += 1
				print(case_list)
				print(date_list)
				print(state_list)	
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None


	def getCasesPerCapita1State(self, state, date, casetype):
			'''
			Returns the number of cases per capita for the specified state on the specified date.
			PARAMETERS:
				state
				date (default: last updated day)
                casetype 
			RETURN:
				the number of cases per capita for the specified state on the specified date
			'''
			last_updated_day = '2020-05-04 20:00:00'	
			array = []
			try: 
				cursor =self.connection.cursor()
				query1 = "SELECT population FROM population WHERE state = '"+ state +"';"
				cursor.execute(query1)
				tuple1 = cursor.fetchone()
				statePopulation = float(tuple1[0])
				array.append(statePopulation)

				query2 = "SELECT "+casetype + " FROM alldatausa WHERE date = '"+ last_updated_day +"' AND place = '"+ state +"';"
				cursor.execute(query2)
				tuple2 = cursor.fetchall()
				stateCase = float(tuple2[0][0])
				array.append(stateCase)

				capita = float(stateCase / statePopulation)
				array.append(capita)
				
				return array 

			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None	
				
	def getCasesPerCapitaAllStates (self, date, casetype):
			'''
			Returns the number of cases per capita for all states in descending order.
			PARAMETERS:
				date (default: last updated day)
				casetype
			RETURN:
				a table of the number of cases per capita for all states on the specified 
				date, i.e State; # of <casetype> cases/capita
			'''
			last_updated_day = '2020-05-04 20:00:00' 
			state_list =[]
			case_list = []
			try:
				cursor = self.connection.cursor()
				query1 = "SELECT place, " + casetype + " FROM alldatausa WHERE date = '"+ last_updated_day +"';"
				cursor.execute(query1)
				pholder = cursor.fetchall()
				print(pholder)
				i = 0
				while i < len(pholder):
					row = pholder[i]
					num_of_cases = float(row[1])
					state = row[0]
					#error handling for differences between population data and case data
					if state == 'Veteran Affair' or state =='US Military' or state == 'Guam' or state == 'Diamond Princess' or state == 'Grand Princess' or state == 'Wuhan Evacuee' or state == 'United States Virgin Islands' or state == 'Northern Mariana Islands':
						i += 1
					#encoding Navajo Nation population here
					elif state == 'Navajo Nation':
						state_list.append(state)
						state_pop = float(173667)
						per_cap = float(num_of_cases/state_pop)
						case_list.append(per_cap)
						i += 1
					elif state == 'Federal Bureau of Prisons':
						state_list.append(state)
						state_pop = float(170400)
						per_cap = float(num_of_cases/state_pop)
						case_list.append(per_cap)
						i += 1
					
					else:
						state_list.append(state)
						print(state)
						query2 = "SELECT population FROM population WHERE state = '"+ row[0] +"';"
						cursor.execute(query2)
						tuple = cursor.fetchone()
						state_pop = float(tuple[0])
						per_cap = float(num_of_cases/state_pop)
						case_list.append(per_cap)
						i += 1
				print("made it out of loop")
				per_cap_array = np.array(state_list, case_list)
				return per_cap_array
				
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None			
				

if __name__ == "__main__":
	datasource = DataSource("subramanianr", "lamp843chair")
	casesInCalifornia = datasource.getCasesOnState("California")
	print ("Results for California")
	for case in casesInCalifornia:
		print case[0]
	
	print ("-------------------------------------------------")
	print ("Recovered")
	casesByType = datasource.getCasesByType("recovered")
	for data in casesByType:
		print data
	
	print ("-------------------------------------------------")
	print ("Results from 2020-05-01 20:00:00 to 2020-05-04 20:00:00")
	casesInDateRange = datasource.getCasesInDateRange('2020-05-01 20:00:00', '2020-05-04 20:00:00')
	for data in casesInDateRange:
		print data
	
	print ("-------------------------------------------------")
	print ("Results FOR CAPITA 1 state")
	casesPERCAPITA = datasource.getCasesPerCapita1State('Alabama','2020-05-01 20:00:00', 'confirmed')
	print('Alabama')
	print casesPERCAPITA
		
	print("-------------------------------------------------")
	print("Results per capita all states")
	allresults = datasource.getCasesPerCapitaAllStates('2020-05-01 20:00:00', 'recovered')
	print allresults

