import math
from PIL import Image
import random

class KMeans:

	def __init__(self):
		self.data = []

	def __init__(self, K, training_num, features_num, training_set, centroids):
		self.K = K
		self.training_num =  training_num
		self.features_num = features_num
		self.training_set = training_set
		self.centroids = centroids
		self.prev_J = 0
		self.J = 0

	def iteration(self):

		self.prev_J = self.J

		cluster_assignments = []
		new_centroids = []

		# initialize cluster_assignments and new_centroids
		for i in range (0, self.K + 1):
			cluster_assignments.append([])
			new_centroids.append([float(0) for i in range(0, self.features_num)])

		# main loop traversing the training_set	
		for index1, data  in enumerate(self.training_set):
			minimum = 0
			cluster = 0

			for index2, centroid in enumerate(self.centroids):
				tmp = 0

				# accumulate all of the computed square of distance between each element to the centroids
				for x in range(0, self.features_num):
					# formula to compute the distance between each feature 
					# to its corresponding centroid feature
					tmp = tmp + ((data[x]-centroid[x]) ** 2)

				tmp = math.sqrt(tmp)

				# keep track of the minimum distance between a specific element to a centroid
				# if the centroid is the first in the array, it's assumed as the minimum
				if index2 == 0:
					minimum = tmp
				elif tmp < minimum:
					minimum = tmp
					cluster = index2

			
			#accumulate the minimum distance for every element in the dataset
			self.J = self.J + minimum
			# keep track of the all the elements within a cluster by storing the index of element
			cluster_assignments[cluster].append(index1)

			# loop to accumulate all the same features of a cluster
			for index3, feature in enumerate(self.training_set[index1]):
				new_centroids[cluster][index3] = new_centroids[cluster][index3] + self.training_set[index1][index3]



		for index4 in range(0, len(new_centroids)):
			for index5 in range(0, self.features_num):
				if len(cluster_assignments[index4]) > 0:
					# get the average of the features for the new centroids
					new_centroids[index4][index5] = new_centroids[index4][index5] / len(cluster_assignments[index4])
		
		
		self.J = self.J / len(self.training_set)
		self.centroids = new_centroids

		return cluster_assignments

############################# MAIN FOR PART 1 ##################################################

def main1 ():
	training_set = []
	file = open("data\kmdata1.txt", "r")


	for line in file:
		training_set.append([float(i) for i in line.split()])


	centroids = [[3,3], [6,2], [8,5]]
	part_one = KMeans(2, 300, 2, training_set, centroids)

	for i in range (0, 10):
		curr_centroids = list(part_one.centroids)
		ca = part_one.iteration()

		ca_file = open("output\iter%d_ca.txt" % (i+1), "w+")

		for j in range(0, len(training_set)):
			for x in range(0, len(ca)):
				if j in ca[x]:
					ca_file.write("%d\n" % (x+1))

		ca_file = open("output\iter%d_cm.txt" % (i+1), "w+")

		for x in range(0,part_one.K+1):
			for y in range(0,part_one.features_num):
				ca_file.write("%f " % part_one.centroids[x][y])
			ca_file.write("\n")

		ca_file.write("J=%f\n" % part_one.J)
		ca_file.write("dJ=%f\n" % (part_one.J - part_one.prev_J))
		ca_file.close()

###########################PART 2 #################################################

class ImageExtraction:

	def __init__(self):
		self.data = []

	# initialization with filename
	def __init__(self, filename):
		self.data = []
		self.file_name = filename
		self.img = Image.open(filename, 'r')
		self.pixels = []

	# extract RGB from image and store in pixels
	def extractRGB(self):
		self.pixels = list(self.img.getdata())
		


########################### MAIN FOR PART 2 #################################################

def centroidRandomizer(num, arr):

	centroids = [];

	while len(centroids) < num:
		# generate random number
		r = random.randint(0, len(arr))

		# check if the random number is already in centroids
		# add if it's not in the centroids
		if arr[r] not in centroids:
			centroids.append(arr[r])

	return centroids

def main2 ():
	imgExtraction = ImageExtraction('data\kmimg1.png')

	imgExtraction.extractRGB()

	part_two = KMeans(16, len(imgExtraction.pixels), 3, imgExtraction.pixels, centroidRandomizer(16, imgExtraction.pixels))
	ca = []

	# run the KMeans iteration 10 times
	for i in range (0, 10):
		ca = part_two.iteration()

	for i in range (0, len(part_two.centroids)):

		# round off the centroids to the nearest integer
		for j in range (0, len(part_two.centroids[i])):
			part_two.centroids[i][j] = int(round(part_two.centroids[i][j]))

		# the value of every pixel assigned to a cluster
		# is converted to the value of the centroid 
		for k in range (0, len(ca[i])):
			imgExtraction.pixels[ca[i][k]] = tuple(part_two.centroids[i])


	# convert the list to image
	img2 = Image.new(imgExtraction.img.mode, imgExtraction.img.size)
	img2.putdata(imgExtraction.pixels)
	img2.save('data\compressed.png')

# if you want to run the part 1 of the lab
# main1()
# if you want to run the part 2 of the lab
main2()