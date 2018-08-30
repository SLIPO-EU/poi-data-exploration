# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 11:27:34 2018

@author: Pantelis Mitropoulos
"""
import pandas as pd
import re
import json
from statistics import *
import sys
import time

class StatsWrapper(object):
	"""
	Collection of tools for statistics wrapper.
	"""

	errors = []
	status = 1

	def get_valid_filename(self, s):
		"""
		A simple method to construct valid filenames.
		"""
		s = str(s).strip().replace(' ', '_')
		return re.sub(r'(?u)[^-\w.]', '', s)

	def reduceOther(self, data):
		"""
		A method to collect all categories with values below a threshold into a unique category named 'other'.
		"""
		total = data.value.sum()
		limit = int(round(0.04*total, 0))
		x_list = data.query('value >= ' + str(limit))
		below_limit = data.query('value < ' + str(limit))
		below_count = below_limit['name'].count()
		if below_count > 0:
			label = 'other (' + str(below_count) + ')' if below_count > 1 else below_limit.iloc[0]['name']
			new = pd.DataFrame([[label, below_limit['value'].sum()]], columns=['name', 'value'])
			x_list = x_list.append(new)
		return x_list

	def extractArgs(self, argv):
		"""
		A method to extract arguments, validate them, and write corresponding messages.
		"""
		args = {}
		for arg in argv:
			key = arg.split('=')[0]
			if key not in [argv[0], 'filename', 'column', 'category', 'chart_type', 'delimiter']:
				self.errors.append('Unknown option: ' + key)
			elif key != 'eval.py':
				args[key] = arg
		try:
			filename = args['filename'].split('=')[1]
		except:
			self.errors.append('Filename should be supplied')
			self.status = 0
		if (self.status == 1):
			try:
				delimiter = args['delimiter'].split('=')[1]
			except:
				delimiter = ','
			try:
				column = args['column'].split('=')[1]
			except:
				column = False
			try:
				category = args['category'].split('=')[1]
			except:
				category = 'generic' if column not in ['name', 'address', 'cost', 'schedule', 'phone', 'rating'] else column
			try:
				chart_type = args['chart_type'].split('=')[1]
			except:
				chart_type = 'bar' if column in ['categorical', 'schedule', 'category', 'rating', 'cost'] else 'pie'
		self.args = {'filename': filename, 'column': column, 'category': category, 'chart_type': chart_type, 'delimiter': delimiter}
		return self.args

	def readCSV(self, args):
		"""
		A method to read a csv file and check for a column existence.
		"""
		try:
			self.df = pd.read_csv(args['filename'], encoding='utf-8', delimiter=args['delimiter'], low_memory=False, engine='c')
			self.shape = self.df.shape
			self.headers = list(self.df)
			if args['column'] != False and args['column'] not in self.headers:
				self.errors.append('Column ' + args['column'] + ' not found in ' + args['filename'])
				args['column'] = False
		except FileNotFoundError:
			self.errors.append('File not found!')
			self.status = 0

	def generalStats(self, dataframe, columns):
		"""
		A method to extract distinct values of a field.
		"""
		children = []

		for column in columns:
			col = self.df[column]
			col = col.astype('str')
			col = col.str.split("|").apply(pd.Series).stack().reset_index(drop=True)
			col = col.str.strip()

			distinct = col.value_counts()
			distinct = distinct.to_frame()
			distinct.columns = ['value']
			distinct.index.name = 'name'
			distinct = distinct.reset_index()
			distinct = distinct.to_dict('records')
			child = {"name": column}
			if float(len(distinct)) <= 30:
				child["children"] = distinct
			children.append(child)

		return children

	def prepare(self, col):
		"""
		Prepare column in case of string data.
		"""
		if (col.dtype == 'object'):
			col = col.str.split("|").apply(pd.Series).stack().reset_index(drop=True)
			col = col.str.strip()
		return col

	def describe(self, col):
		"""
		Enhanced description based on pandas describe.
		"""
		isnull = col.isnull().value_counts()
		try:
			null = isnull[True]
		except:
			null = 0

		if (col.dtype == 'object'):
			length = col.apply(str).map(len)
			minimum = length.min()
			maximum = length.max()
			desc = col.describe()
			if desc["freq"] < 3:
				del desc["freq"]
				del desc["top"]
			desc["null"] = null
			desc["minimum length"] = minimum
			desc["maximum length"] = maximum
		else:
			desc = col.describe()
			desc["null"] = null
		for key, value in desc.iteritems():
			try:
				desc[key] = int(value)
			except:
				try:
					desc[key] = float(value)
				except:
					pass

		return desc

	def clear(self):
		del self.df
		return

"""
Main ...
"""
if __name__ == "__main__":
	start_time = time.time()
	wrapper = StatsWrapper()
	args = wrapper.extractArgs(sys.argv)
	if (wrapper.status == 1):
		wrapper.readCSV(args)

	# end_time = time.time()
	# print("--- %s seconds ---" % (end_time - start_time))
	# exit()

	column = args['column']
	category = args['category']
	chart_type = args['chart_type']

	general = {
		'status': wrapper.status,
		'filename': args['filename'],
		'rows': wrapper.shape[0],
		'columns': wrapper.shape[1],
		'headers': wrapper.headers,
		'errors': wrapper.errors
	} if len(wrapper.errors)==0 else {
		'status': wrapper.status,
		'errors': wrapper.errors
	}

	if general['status'] == 1:
		# start_time = time.time()

		if column == False:
			unique = {"name": args['filename']}
			unique["children"] = wrapper.generalStats(wrapper.df, wrapper.headers)
			data = {"general": general, "list": wrapper.headers, "unique": unique}
			end_time = time.time()
			with open('./output/' + 'data.json', 'w') as fp:
				json.dump(data, fp, ensure_ascii=False, indent=2)

		else:
			specific_data = pd.DataFrame()
			col = wrapper.df[column]
			wrapper.clear();
			print('Memory cleared')
			col = wrapper.prepare(col)

			specific_data["description"] = wrapper.describe(col)
			specific_data = specific_data.to_dict()

			if category == 'categorical':
				stats = Categorical(col, chart_type)
				stats.reduceOther(stats.chart)

			elif category == 'schedule':
				stats = Schedule(col, chart_type)

			elif category == 'name':
				stats = Name(col, chart_type)
				stats.reduceOther(stats.chart)

			elif category == 'cost':
				stats = PriceRange(col, chart_type)

			elif category == 'address':
				stats = Address(col, chart_type)
				print(stats.chart)

			elif category == 'phone':
				stats = PhoneNumber(col, chart_type)

			elif category == 'rating':
				stats = Ratings(col, chart_type)
				stats.reduceOther(stats.chart)

			else:
				category = 'generic'
				stats = RegexStats(col, chart_type)
				stats.reduceOther(stats.chart)

			specific_data[category] = stats.chart

			end_time = time.time()
			json_filename = wrapper.get_valid_filename(column + ".json")
			with open('./output/' + json_filename, 'w') as fp:
				json.dump(specific_data, fp, ensure_ascii=False, indent=2)

		print("--- %s seconds ---" % (end_time - start_time))

	else:
		with open('./output/' + 'data.json', 'w') as fp:
			json.dump(general, fp, ensure_ascii=False, indent=2)