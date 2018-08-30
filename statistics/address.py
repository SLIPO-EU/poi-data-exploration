import pandas as pd
import re as regex
import numpy as np
from collections import OrderedDict
from .statistics import Statistics

class Address(Statistics):
	"""	Tools to extract address patterns and distribute the values accross known patterns."""

	re_words = '(?:(?:(?:[^0-9]*[0-9]+[^0-9]{1,2}\s[^0-9]+)+)|(?:[^0-9]+))(?=\s|$)'
	"""	Words regular expression (language independent), e.g. street name, city etc."""

	re_number = '(?:[0-9\-]+[ABCDabcdΑΒΓΔαβγδ]{0,1})'
	"""	Street number regular expression."""

	re_pc = '(?:\d{5}([\-]\d{4})?)|(?:[0-9]{4})|(?:[0-9]{5}[\-]?[0-9]{3})|(?:[A-Za-z][0-9][A-Za-z] [0-9][A-Za-z][0-9])|(?:[0-9]{3,4})|(?:[1-9][0-9]{3}\s?[a-zA-Z]{2})|(?:[0-9]{5})|(?:\d{3}-\d{4})|(?:(L\s*(-|—|–))\s*?[\d]{4})|(?:[0-9]{2}\-[0-9]{3})|(?:((0[1-9]|5[0-2])|[1-4][0-9])[0-9]{3})|(?:\d{3}\s?\d{2})|(?:[A-Za-z]{1,2}[0-9Rr][0-9A-Za-z]? [0-9][ABD-HJLNP-UW-Zabd-hjlnp-uw-z]{2})'
	"""	Postal code regular expression."""

	re_space = '(?:\s+)'
	""" A regular expression for space(s)."""

	re_symbols = '[\-\`\~\!\@\#\$\%\^\&\*\(\)\_\+\[\]\{\}\;\:\"\'\\\,\.\<\>\/\?€]+'
	"""	Symbols regular expression"""

	patterns = [
			('words + number', re_words + re_space + re_number),
			('words + number + words + number', re_words + re_space + re_number + re_words + re_space + re_number),
			('words + number + words + number + words', re_words + re_space + re_number + re_words + re_space + re_number + re_words),
			('words + number + words', re_words + re_space + re_number + re_words),
			('words + number + words + postal code + words', re_words + re_space + re_number + re_words + re_space + re_pc + re_words),
			('words + number + postal code', re_words + re_space + re_number + re_space + re_pc),
			('words + number + words + number + postal code', re_words + re_space + re_number + re_words + re_space + re_number + re_space + re_pc),
			('words + number + postal code + words', re_words + re_space + re_number + re_space + re_pc + re_words),
			('words + number + words + number + postal code + words', re_words + re_space + re_number + re_words + re_space + re_number + re_space + re_pc + re_words),
			('number + words', re_number + re_words),
			('number + words + number + words', re_number + re_words + re_space + re_number + re_words),
			('number + words + postal code', re_number + re_words + re_space + re_pc),
			('number + words + number + words + postal code', re_number + re_words + re_space + re_number + re_words + re_space + re_pc),
			('number + words + number + words', re_number + re_words + re_space + re_number + re_words),
			('number + words + number + words + postal code + words', re_number + re_words + re_space + re_number + re_words + re_space + re_pc + re_words),
			('words', re_words)
		]
	"""	Various possible patterns for address."""

	def __init__(self, series, chart_type='pie'):
		"""
		Address Class initialization.

		Place the patterns in an ordered dictionary (order is important in pattern search),
		and subsequently compare each the pattern against the series values.
		"""
		super().__init__(series, chart_type)
		self.patterns = OrderedDict(self.patterns)
		super().checkPatterns(series, self.patterns)
