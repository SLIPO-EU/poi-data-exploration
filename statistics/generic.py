# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 08:51:14 2018

@author: Pantelis Mitropoulos

This module constructs the pattern of generic data, and extracts useful
statistics about pattern distribution. It is agnostic to the data nature.
"""

import pandas as pd
import re as regex
import numpy as np
from .statistics import Statistics


class RegexStats(Statistics):

	__groups = {
			'el': '\ ςερτυθιοπασδφγηξκλζχψωβνμΕΡΤΥΘΙΟΠΑΣΔΦΓΗΞΚΛΖΧΨΩΒΝΜέύίόάήώϋΰϊΐΈΎΊΌΆΉΫΪ',
			'en': '\ a-zA-Z',
			'num': '0-9',
			'sym': '\-\`\~\!\@\#\$\%\^\&\*\(\)\_\+\[\]\{\}\;\:\"\'\\\,\.\<\>\/\?€’'
			}
	"""	The various groups of characters."""

	__languages = {
			'el': 'greek',
			'en': 'english'
		}
	"""	The corresponding user friendly name of the above groups."""

	def __init__(self, inputSeries, chart_type='pie'):
		"""
		This class constructs a ......
		"""
		super().__init__(inputSeries, chart_type)
		col = inputSeries;
		while col.size > 0:
			strg = str(col[0])
			entry = self.stats(strg)
			match = col.str.match(self.regex)
			row = {}
			row["value"] = int(match.value_counts()[1])
			row["name"] = " + ".join(self.description) + " + " + "\nE.g.:" + strg
			self.append(row)
			col = pd.Series([col[index] for index, cond in match.iteritems() if not cond])


	def stats(self, strg):
		self.pattern = self.constructPattern(strg)
		compiled_pattern = self.__compilation(self.pattern)
		self.regex = self.constructRegex(compiled_pattern)
		self.description = self.constructDescription(compiled_pattern)

	def __repr__(self):
		"""
		The represantation of the object.
		"""
		output = "Regex: " + str(self.regex) + "\n"
		output += "Pattern: " + str(self.pattern) + "\n"
		output += "Desc: " + str(self.description) + "\n"
		return output

	def __str__(self):
		"""
		The user friendly print of the object.
		"""
		return self.__repr__()

	def __compilation(self, array):
		"""
		Private method to compile values in an array to distinct
		ones in case they are subsequently the same.
		"""
		result = []
		previous = ''
		for value in array:
			if value != previous:
				result.append(value)
				previous = value
		return result

	def constructPattern(self, strg):
		"""
		Given a string, it constructs a pattern according to the
		pattern groups defined above.
		"""
		groups = self.__groups
		try:
			words = strg.split(' ')
		except:
			words = [str(strg)]
		result = [[] for index in words]
		words = pd.Series(words)
		while (words.size > 0):
			for key in groups:
				pattern = '(?:^['+groups[key]+']+)'
				match = words.str.contains(pattern)
				for index, cond in match.iteritems():
					if cond:
						if key == 'num':
							p = regex.compile('([0-9]{1,})')
							num_match = p.findall(words[index])
							size = len(num_match[0])
						elif key == 'sym':
							p = regex.compile('(['+groups['sym']+']+)')
							sym_match = p.findall(words[index])
							symbol = sym_match[0]
						entry = size if key=='num' else key
						entry = symbol if key=='sym' else entry
						result[index].append(entry)
				words = words.str.replace(pattern, '', 1)
				words.replace('', pd.np.nan, inplace=True)
				words.dropna(inplace=True)
				if words.size == 0:
					break;
		return result

	def constructRegex(self, pattern):
		"""
		Given a pattern, it constructs the corresponding regural expression.
		"""
		groups = self.__groups
		result = []
		for words in pattern:
			p = ''
			for attr in words:
				if isinstance(attr, int):
					p += '(?:['+groups['num']+']{'+str(attr)+'})'
				elif attr in groups:
					p += '(?:['+groups[attr]+']+)'
				else:
					p += '(?:'
					for c in attr:
						p += "\\" + c
					p += ')'
			result.append(p)
		result = "\ ".join(result)
		return result

	def constructDescription(self, pattern):
		"""
		Given a pattern, it constructs a user friendly description.
		"""
		result = []
		for word in pattern:
			desc = '';
			if len(word) > 1:
				desc += 'mixed '
				index = 0
				for chars in word:
					if isinstance(chars, int):
						desc += 'numeric (len. ' + str(chars) + ')'
					elif chars in self.__languages.keys():
						desc += self.__languages[chars]
					else:
						desc += 'symbol (' + chars + ')'
					if index < len(word) - 2:
						desc += ', '
					elif index == len(word) - 2:
						desc += ' and '
					else:
						desc += ' characters'
					index += 1
			else:
				chars = word[0]
				if isinstance(chars, int):
					desc += 'length ' + str(chars) + ' numeric'
				elif chars in self.__languages.keys():
					desc += self.__languages[chars] + ' word(s)'
				else:
					desc += 'symbol(s): ' + chars
			result.append(desc)
		return result