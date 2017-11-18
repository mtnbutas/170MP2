import math

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


training_set = []
file = open("C:\Users\TRISHA NICOLE\Desktop\Machine Problem 2\kmdata1.txt", "r")


for line in file:
	training_set.append([float(i) for i in line.split()])


centroids = [[3,3], [6,2], [8,5]]
part_one = KMeans(2, 300, 2, training_set, centroids)

for i in range (0, 2):
	curr_centroids = list(part_one.centroids)
	ca = part_one.iteration()

	ca_file = open("iter%d_ca.txt" % (i+1), "w+")

	for j in range(0, len(training_set)):
		for x in range(0, len(ca)):
			if j in ca[x]:
				ca_file.write("%d\n" % (x+1))

	ca_file = open("iter%d_cm.txt" % (i+1), "w+")

	for x in range(0,part_one.K+1):
		for y in range(0,part_one.features_num):
			ca_file.write("%f " % part_one.centroids[x][y])
		ca_file.write("\n")

	ca_file.write("J=%f\n" % part_one.J)
	ca_file.write("dJ=%f\n" % (part_one.J - part_one.prev_J))
	ca_file.close()
