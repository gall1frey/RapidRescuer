
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1A of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ 492 ]
# Author List:		[ Mallika Sirdeshpande, Aryan Sharma, Atharva Gupta, Toshani Rungta ]
# Filename:			task_1a.py
# Functions:		readImage, solveMaze
# 					[ find_n, wt, z_ex, shortestpath, checkn ]
# Global variables:	CELL_SIZE
# 					[ List of global variables defined in this file ]


# Import necessary modules
# Do not import any other modules
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Maze images in task_1a_images folder have cell size of 20 pixels
CELL_SIZE = 20


def readImage(img_file_path):

	"""
	Purpose:
	---
	the function takes file path of original image as argument and returns it's binary form

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image

	Returns:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path

	Example call:
	---
	original_binary_img = readImage(img_file_path)

	"""

	binary_img = None

	#############	Add your Code here	###############
	
	img = cv2.imread(img_file_path,0)
	ret,binary_img = cv2.threshold(img,20,250,cv2.THRESH_BINARY)

	###################################################

	return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

	"""
	Purpose:
	---
	the function takes binary form of original image, start and end point coordinates and solves the maze
	to return the list of coordinates of shortest path from initial_point to final_point

	Input Arguments:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path
	`initial_point` :		[ tuple ]
		start point coordinates
	`final_point` :			[ tuple ]
		end point coordinates
	`no_cells_height` :		[ int ]
		number of cells in height of maze image
	`no_cells_width` :		[ int ]
		number of cells in width of maze image

	Returns:
	---
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Example call:
	---
	shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

	"""
	
	shortestPath = []

	#############	Add your Code here	###############
	
	pos_maze = wt(final_point,no_cells_width,no_cells_height,original_binary_img)
	shortestPath = shortestpath(original_binary_img,pos_maze,initial_point,final_point,no_cells_width,no_cells_height)

	###################################################
	
	return shortestPath


#############	You can add other helper functions here		#############


def find_n(pic,coord_array,max_r,max_c):
	m,ns = [],[]
	if type(coord_array) == tuple:
		m.append(coord_array)
	else: m = coord_array
	for i in m:
		r = i[0]
		c = i[1]
		n = []
		#up wall
		x = (r)*CELL_SIZE-1
		y = (c)*CELL_SIZE-1
		if r == 0:
			s = (pic[x+1:x+7,y+5:y+15]==0).sum()
		else:
			s = (pic[x-2:x+5,y+7:y+13]==0).sum()	
		if s == 0:
			n.append((r-1,c))

		#down wall
		x = (r+1)*CELL_SIZE-1
		y = (c)*CELL_SIZE-1
		if r == max_r:
			s = (pic[x-5:,y+5:y+15] == 0).sum()
		else:
			s = (pic[x-2:x+5,y+7:y+13] == 0).sum()
		if s == 0:
			n.append((r+1,c))

		#left wall
		x = (r)*CELL_SIZE-1
		y = (c)*CELL_SIZE-1
		if c == 0:
			s = (pic[x+5:x+15,y+1:y+5] == 0).sum()
		else:
			s = (pic[x+7:x+13,y-2:y+5] == 0).sum()
		if s == 0:
			n.append((r,c-1))

		#Right Wall
		x = (r)*CELL_SIZE-1
		y = (c+1)*CELL_SIZE-1
		if c == max_c:
			s = (pic[x+5:x+15,y-5:] == 0).sum()
		else:
			s = (pic[x+7:x+13,y-5:y+5] == 0).sum()
		if s == 0:
			n.append((r,c+1))
		ns.extend(n)
	return ns

def wt(stop,r,c,pic):
	been = []
	ad = 1
	A = [[0 for i in range(r)] for j in range(c)]
	x = [stop]
	A[stop[0]][stop[1]] = ad
	been.append(stop)
	while len(x) > 0:
		#print('ad=',ad)
		#print(len(been))
		#print(x,been,'',sep='\n')
		ad += 1
		y = find_n(pic,x,r,c)
		y = list(set(y)-set(been))
		x.clear()
		y = list(filter(lambda i: i[0] < r and i[1] < c and i[0] >= 0 and i[1] >= 0,y))
		for i in y:
			A[i[0]][i[1]] = ad
			x.append(i)
			been.append(i)
	return A
            
def z_ex(m):
    for i in m:
        if 0 in i:
            return True
    return False

def shortestpath(pic,wm,s,e,r,c):
	current = s
	path = []
	path.append(current)
	#print(type(current))
	#print(wm[current[0]][current[1]])
	while wm[current[0]][current[1]] > 1:
		current = checkn(pic,wm,current,r,c)
		path.append(current)
	return path

def checkn(pic,m,coord,r,n):
	l = find_n(pic,coord,r,n)
	#print(l)
	v = {}
	for i in l:
		v[m[i[0]][i[1]]] = i
		small = min(v)
	return v[small]

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1a_images/'				# path to directory of 'task_1a_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')


