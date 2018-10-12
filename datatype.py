class DataType():

	def __init__(self, datatype):
		self.datatype = datatype
		self.counter = 0


	# used to give the name of file and increses the counter
	def counter_name(self):
		name = self.datatype + " " + str(self.counter)
		self.counter += 1
		return name

