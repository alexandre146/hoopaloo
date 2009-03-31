# coding: utf-8
"""
Extra HTML Widget classes
"""

import datetime
from datetime import date
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from hoopaloo.util import get_next_friday

__all__ = ('SelectDateWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?) (\d\d?):(\d\d?)$')

HOUR_LIST = ['23:59', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30',
'10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:56', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
class SelectDateWidget(Widget):
	"""
	A Widget that splits date input into three <select> boxes.
	This also serves as an example of a Widget that has more than one HTML
	element and hence implements value_from_datadict.
	"""
	month_field = '%s_month'
	day_field = '%s_day'
	year_field = '%s_year'
	hour_field = '%s_hour'
	
	
	def __init__(self, attrs=None, years=None):
        # years is an optional list/tuple of years to use in the "year" select box.
		self.attrs = attrs or {}
		if years:
			self.years = years
		else:
			this_year = datetime.date.today().year
			self.years = range(this_year, this_year+10)
			
	
	def render(self, name, value, attrs=None):
		try:
			year_val, month_val, day_val, hour_val, minute_val = value.year, value.month, value.day, value.hour
		except AttributeError:
			year_val = month_val = day_val = hour_val = min_val = None
			if isinstance(value, basestring):
				match = RE_DATE.match(value)
				if match:
					year_val, month_val, day_val, hour_val, min_val = [int(v) for v in match.groups()]
		
		output = []
		
		if 'id' in self.attrs:
			id_ = self.attrs['id']
		else:
			id_ = 'id_%s' % name

		nx_fr = get_next_friday(date.today())
		month_choices = MONTHS.items()
		month_choices.sort()
		local_attrs = self.build_attrs(id=self.month_field % id_)
		
		select_html = Select(choices=month_choices).render(self.month_field % name, month_val, local_attrs)
		output.append(select_html)
		
		day_choices = [(i, i) for i in range(1, 32)]
		local_attrs['id'] = self.day_field % id_
		select_html = Select(choices=day_choices).render(self.day_field % name, day_val, local_attrs)
		output.append(select_html)

		year_choices = [(i, i) for i in self.years]
		local_attrs['id'] = self.year_field % id_
		select_html = Select(choices=year_choices).render(self.year_field % name, year_val, local_attrs)
		output.append(select_html)
		
		hour_choices = [(i, i) for i in HOUR_LIST]
		local_attrs['id'] = self.hour_field % id_
		h_val = hour_val, ':', min_val
		select_html = Select(choices=hour_choices).render(self.hour_field % name, h_val, local_attrs)
		output.append(select_html)
		
		return mark_safe(u'\n'.join(output))

	def id_for_label(self, id_):
		return '%s_month' % id_
		
	id_for_label = classmethod(id_for_label)

	def value_from_datadict(self, data, files, name):
		y, m, d, h = data.get(self.year_field % name), data.get(self.month_field % name), data.get(self.day_field % name), data.get(self.hour_field % name)
		if y and m and d:
			return '%s-%s-%s %s' % (y, m, d, h)
		return data.get(name, None)
		
			