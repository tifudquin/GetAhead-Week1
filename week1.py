import collections
from typing import Deque
from itertools import islice, cycle

class BidirectionalIterator:
	def __init__(self, iterables):
		self.iterables = iterables
		self.index = 0

	def __iter__(self):
		return self

	def __next__(self):
		i = self.index
		self.index += 1
		try:
			values = self.iterables[i]
			return values
		except IndexError:
			raise StopIteration

	def __prev__(self):
		i = self.index
		self.index -= 1
		try:
			values = self.iterables[i]
			return values
		except IndexError:
			raise StopIteration


class ListBidiretionalIterator(BidirectionalIterator):
	def __init__(self, iterators):
		self.iterators = iterators
		self.index = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self.index == len(self.iterators):
			raise StopIteration
		else:
			i = self.index
			self.index += 1
			return self.iterators[i]

	def __prev__(self):
		if self.index == 0:
			raise StopIteration
		else:
			i = self.index
			self.index -= 1
			return self.iterators[i]


class FlattenedBidirectionalIterator:
	def __init__(self, iterators):
		self.forward = collections.deque(self.roundrobin(iterators))
		self.backward = collections.deque([])
		self.tempForward = None
		self.tempBackward = None

	# Method that merges all iterators in an interleaved fashion
	def roundrobin(self, iterators):
		pending = len(iterators)
		nexts = cycle(it.__iter__().__next__ for it in iterators)
		while pending:
			try:
				for next in nexts:
					yield next()
			except StopIteration:
				pending -= 1
				nexts = cycle(islice(nexts, pending))

	def __iter__(self):
		return self

	def __next__(self):
		while self.forward:
			if self.tempForward != None or self.tempBackward == None:
				# Append tempForward to self.backward
				# No need to empty tempFoward variable because content will be replaced in try
				self.backward.appendleft(self.tempForward)
			try:
				# Put back tempBackward to self.backward
				# Then empty tempBackward
				if self.tempBackward != None:
					self.backward.appendleft(self.tempBackward)
					self.tempBackward = None

				iterator = self.forward.popleft()
				self.tempForward = iterator
				return iterator
			except StopIteration:
				pass
			raise StopIteration

	def __hasNext__(self):
		if len(self.forward) == 0:
			return False
		else: 
			return True

	def __prev__(self):
		while self.backward:
			if self.tempBackward != None or self.tempForward == None:
				# Append tempBackward to self.forward
				# No need to empty tempBackward variable because content will be replaced in try
				self.forward.appendleft(self.tempBackward)
			try:
				# Put back tempForward to self.forward
				# Then empty tempForward
				if self.tempForward != None:
					self.forward.appendleft(self.tempForward)
					self.tempForward = None

				iterator = self.backward.popleft()
				self.tempBackward = iterator
				return iterator
			except StopIteration:
				pass
			raise StopIteration

	def __hasPrev__(self):
		if len(self.backward) == 0:
			return False
		else:
			return True
