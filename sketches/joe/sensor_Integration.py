

class sensorIntegration(self, roi, dist):
	self.roiWidth = -1
	self.expWidth = -1
	self.isCar = False # when true we can display the actual roi the haar algorithm found 

	def findcar(self):
		self.roiWidth = roi[2]
		lowerLim = 0.9
		upperLim = 1.1

		if self.roiWidth in range(self.roiWidth*lowerLim, self.roiWidth*upperLim ):
			self.isCar = True
			return self.isCar

	def calcExpectedDistance(self):
		# somehow use 'dist' to calulate the expected width

		#sensorWidth = 
		#self.expWidth = , )

		return self.expWidth

# we need a way of importing data: roi and  distance 

testing = sensorIntegration(roi, dist)
testing.findCar()