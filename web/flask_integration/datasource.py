'''
    datasource.py

    A program that acts as the backend of our website that executes queries against the database.

    Gracie Little, Rudra Subramanian, Rebecca Fox, Yemi Shin 
    25 May 2020
    CS257
'''
import psycopg2
import getpass
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from datetime import timedelta
 

class DataSource:

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
				query = "SELECT confirmed FROM alldatausanew WHERE place =" +"'" + state +"' and date = "+ lastUpdate +";"
				cursor.execute(query)
				return cursor.fetchall()
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None


	def getCasesByType(self, casetype, date='2020-05-04 20:00:00'):
			'''
			Returns the number of accumulated COVID-19 cases by its type.
			PARAMETERS:
				type - confirmed, recovered, death
				date - (default: last updated day)
			RETURN:
				the number of accumulated COVID-19 cases by its type
			'''

			try:
				cursor = self.connection.cursor()
				query = "SELECT place, " + casetype + " FROM alldatausanew WHERE date = '" + date + "';"
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
				query = "SELECT * FROM alldatausa WHERE date between '" + start + "' AND '" + end + "';"
				results = cursor.execute(query)
				# FINISH HERE
				return cursor.fetchall()
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None


	def getCasesPerCapita1State(self, state, casetype):
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
				#print("here?")
				query2 = "SELECT " + casetype + " FROM alldatausanew WHERE date = '"+ last_updated_day +"' AND place = '"+ state +"';"
				cursor.execute(query2)
				tuple2 = cursor.fetchall()
				stateCase = float(tuple2[0][0])
				array.append(stateCase)
				#print("here2?")
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
			last_updated_day = '2020-05-25' 
			state_list =[]
			case_list = []
			state_pop_list = []
			try:
				cursor = self.connection.cursor()
				query1 = "SELECT place, " + casetype + " FROM alldatausanew WHERE date = '"+ date +"';"
				cursor.execute(query1)
				pholder = cursor.fetchall()
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
						state_pop_list.append(state_pop)
						per_cap = float(num_of_cases/state_pop)
						case_list.append(per_cap)
						i += 1
					elif state == 'Federal Bureau of Prisons':
						state_list.append(state)
						state_pop = float(170400)
						state_pop_list.append(state_pop)
						per_cap = float(num_of_cases/state_pop)
						case_list.append(per_cap)
						i += 1
					
					else:
						state_list.append(state)
						query2 = "SELECT population FROM population WHERE state = '"+ row[0] +"';"
						cursor.execute(query2)
						tuple = cursor.fetchone()
						state_pop = float(tuple[0])
						state_pop_list.append(state_pop)
						per_cap = float(num_of_cases/state_pop)
						case_list.append(per_cap)
						i += 1
				
				self.getPerCapGraph(state_list, case_list)
					
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None	
				
		
	def getCases(self, state, casetype, start, end):
			'''
			Returns the accumulated number of COVID-19 cases in the specified date range.
			PARAMETERS:
				state (default: all)
				casetype - confirmed, death, recovered
				start - the starting date of the range
				end - the ending date of the range
			RETURN:
				the accumulated number of COVID-19 cases in the specified date range
			'''
			#Region lists:
			MW = ['North Dakota', 'South Dakota', 'Minnesota', 'Nebraska', 'Kansas', 'Missouri', 'Illinois', 'Iowa', 'Wisconsin', 'Indiana', 'Michigan', 'Ohio']
			NE = ['Pennsylvania', 'New York', 'New Jersey', 'Delaware', 'Maryland', 'Connecticut', 'Vermont', 'New Hampshire', 'Massachusetts', 'Rhode Island', 'Maine', 'District of Columbia']
			SE = ['Arkansas', 'Louisiana', 'Mississippi', 'Alabama', 'Georgia', 'Florida', 'South Carolina', 'North Carolina', 'Tennessee', 'Kentucky', 'West Virginia', 'Virginia', 'Puerto Rico']
			SW = ['Arizona', 'New Mexico', 'Texas', 'Oklahoma', 'Navajo Nation']
			W = ['Washington', 'Oregon', 'Montana', 'Idaho', 'Wyoming', 'California', 'Nevada', 'Utah', 'Colorado', 'Alaska', 'Hawaii']
			
			try:
				cursor =self.connection.cursor()
				if state == 'All':
					query = "SELECT place, " + casetype + " , date FROM alldatausanew WHERE date between '" + start + "' AND '" + end + "';"
					cursor.execute(query)
					results = cursor.fetchall()
					region_list = []
					i = 0
					
					while i < len(results):
						if results[i][0] in MW:
							region_list.append('MW')
							i += 1
						elif results[i][0] in NE:
							region_list.append('NE')
							i += 1
						elif results[i][0] in SE:
							region_list.append('SE')
							i += 1	
						elif results[i][0] in SW:
							region_list.append('SW')
							i += 1
						elif results[i][0] in W:
							region_list.append('W')
							i += 1
						else:
							region_list.append('Other')
							i += 1
					
					
					labels = ['State', 'Number of Cases', 'Date']
					df = pd.DataFrame.from_records(results, columns = labels)
					df['Region'] = region_list

					df.Date = pd.to_datetime(df['Date'])
					df = df.set_index(['Date'], inplace = False)
					rgrouped = df.groupby('Region')
					regdflist = []
					for group in rgrouped.groups: 
						x = rgrouped.get_group(group)
						regdflist.append(x)
					
					self.getCasesAllGraph(regdflist)	
				
				else:
	
					query = "SELECT " + casetype + ", date FROM alldatausanew WHERE place = '"+ state +"' AND date between '" + start + "' AND '" + end + "';"
					cursor.execute(query)
					
					results = cursor.fetchall()
					print(results)
					labels = ['Number of Cases', 'Date']
					df = pd.DataFrame.from_records(results, columns = labels)
					df = df.set_index(['Date'], inplace = False)
					self.getCasesOneGraph(df, state, casetype)
							
			except Exception as e:
				print ("Something went wrong when executing the query: ", e)
				return None	

				
	def getCasesAllGraph(self, dflist):
		regdflist = dflist
		fig = plt.figure(figsize = (30,30))
		fig.tight_layout()

		if len(regdflist) >= 1:			
			ax1 = fig.add_subplot(231)
			for label, grp in regdflist[0].groupby('State'):
				grp.plot(y='Number of Cases', ax = ax1, label = label)
			ax1.set_title(regdflist[0].Region[0], fontweight = "bold", size = 20)
			ax1.legend(fontsize = 'large')
			ax1.tick_params(labelsize=13)
			plt.savefig("static/datavis.png")

		if len(regdflist) >= 2:	
			ax2 = fig.add_subplot(232)
			for label, grp in regdflist[1].groupby('State'):
				grp.plot(y='Number of Cases', ax = ax2, label = label)
			ax2.set_title(regdflist[1].Region[0], fontweight = "bold", size = 20)
			ax2.legend(fontsize = 'large')
			ax2.tick_params(labelsize=13)
			plt.savefig("static/datavis.png")

		if len(regdflist) >= 3:				
			ax3 = fig.add_subplot(233)
			for label, grp in regdflist[2].groupby('State'):
				grp.plot(y='Number of Cases', ax = ax3, label = label)
			ax3.set_title(regdflist[2].Region[0], fontweight = "bold", size = 20)
			ax3.legend(fontsize = 'large')
			ax3.tick_params(labelsize=13)
			plt.savefig("static/datavis.png")
					
		if len(regdflist) >= 4:	
			ax4 = fig.add_subplot(234)
			for label, grp in regdflist[3].groupby('State'):
				grp.plot(y='Number of Cases', ax = ax4, label = label)
			ax4.set_title(regdflist[3].Region[0], fontweight = "bold", size = 20)
			ax4.legend(fontsize = 'large')
			ax4.tick_params(labelsize=13)
			plt.savefig("static/datavis.png")
					
		if len(regdflist) >= 5:	
			ax5 = fig.add_subplot(235)
			for label, grp in regdflist[4].groupby('State'):
				grp.plot(y='Number of Cases', ax = ax5, label = label)
			ax5.set_title(regdflist[4].Region[0], fontweight = "bold", size = 20)
			ax5.legend(fontsize = 'large')
			ax5.tick_params(labelsize=13)
			plt.savefig("static/datavis.png")
					
		if len(regdflist) == 6:		
			ax6 = fig.add_subplot(236)
			for label, grp in regdflist[5].groupby('State'):
				grp.plot(y='Number of Cases', ax = ax6, label = label)
			ax6.set_title(regdflist[5].Region[0], fontweight = "bold", size = 20)
			ax6.legend(fontsize = 'large')
			ax6.tick_params(labelsize=13)
			plt.savefig("static/datavis.png")
			
		plt.savefig("static/datavis.png")
		
	def getCasesOneGraph(self, dataframe, State, Casetype):
		df = dataframe
		state = State
		casetype = Casetype
		fig, ax = plt.subplots(figsize= (20,20))
		graphlabel = str(state) + ': ' + str(casetype)
		df.plot(y='Number of Cases', use_index = True, label= graphlabel)
		ax.set_title(state, fontweight = "bold", size =30)
		ax.tick_params(axis = 'x', rotation=45)

		plt.savefig("static/datavis.png")
	
	def getPerCapGraph(self, stateList, caseList):
		state_list = stateList
		case_list = caseList
		
		plt.rcdefaults()
		fig, ax = plt.subplots(figsize = (16, 12))
		y_pos = np.arange(len(state_list))
		ax.barh(y_pos, case_list, align='center')
		ax.set_yticks(y_pos)
		ax.set_yticklabels(state_list)
		ax.invert_yaxis() 
		plt.title('Per Capita Cases', size = 30)
		plt.xlabel('Cases per capita')
		plt.xlim(0, .010)
		plt.margins(4.0, 0)
		plt.ylabel('States', fontsize='7')
		plt.savefig("static/datavis.png")			
							
if __name__ == "__main__":
	datasource = DataSource("subramanianr", "lamp843chair")
	
	datasource.getCases('All', 'Confirmed', '2020-02-05', '2020-03-05')
