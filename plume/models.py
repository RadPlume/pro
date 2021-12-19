from django.contrib.gis.db import models


class Reactor(models.Model):
	name = models.CharField(max_length=100)
	location = models.PointField()
	bl = models.PointField()
	br = models.PointField()
	tr =  models.PointField()
	tl = models.PointField()
	extent = models.PolygonField()	

	def __str__():
		return name

