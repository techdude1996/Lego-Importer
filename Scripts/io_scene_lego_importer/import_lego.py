import os
from os import path
import math
import bpy

# Generic function that forwards the file to the appropriate import function
def load_file(self, context):
	src_name, src_ext = os.path.splitext(self.filepath)

	if src_ext == '.ldr' or src_ext == '.dat':
		# If the file is LDraw, send to read_ldraw function
		read_ldraw(self, context, self.filepath)

# LDraw Line specification:
# 0   1     2  3 4 5 6 7 8 9 10 11 12 13  14
# 1 <color> x -z y a b c d e f  g  h  i <part file> (there is actually only one space between each value)

# LDraw Processing Function
def read_ldraw(self, context, src):
	# Debug: print ldraw file to import
	print(src)

	# Open the ldraw file:
	ldraw_file = open(src, "r")

	# If the file was successfully opened, continue processing:
	if ldraw_file.mode == "r":

		ldraw_materials = {'0': (0.020, 0.019, 0.014, 1.000),
		                   '1': (0.000, 0.035, 0.617, 1.000),
						   '2': (0.000, 0.181, 0.000, 1.000),
						   '3': (0.000, 0.175, 0.214, 1.000),
						   '4': (0.584, 0.010, 0.003, 1.000),
						   '5': (0.578, 0.162, 0.352, 1.000),
						   '6': (0.098, 0.041, 0.020, 1.000),
						   '7': (0.328, 0.356, 0.337, 1.000),
						   '8': (0.153, 0.156, 1.107, 1.000),
						   '9': (0.456, 0.644, 0.768, 1.000),
						   '10': (0.030, 0.227, 0.023, 1.000),
						   '11': (0.027, 0.267, 0.333, 1.000),
						   '12': (0.888, 0.105, 0.062, 1.000),
						   '13': (0.973, 0.146, 0.249, 1.000),
						   '14': (1.000, 0.625, 0.004, 1.000),
						   '15': (0.694, 0.694, 0.672, 1.000),
						   '17': (0.305, 1.000, 0.333, 1.000),
						   '18': (0.965, 0.687, 0.687, 1.000),
						   '19': (0.445, 0.238, 0.056, 1.000),
						   '20': (0.597, 0.651, 0.831, 1.000),
						   '22': (0.328, 0.019, 0.468, 1.000),}

		# Since LDraw is a line-based file, read in the whole file as lines:
		ldraw_lines = ldraw_file.readlines()
		# Part counter:
		part_num = 1

		# Get the path of the parts library:
		addons_paths = bpy.utils.script_paths("addons")
		library_path = "library"
		for path in addons_paths:
			library_path = os.path.join(path, "io_scene_lego_importer/Library")
			if os.path.exists(library_path):
				break

		# Proccess each LDraw line:
		for item in ldraw_lines:
			# 3 unit array to store x, y, z transformations
			transform = [None] * 3

			# Split the data row into a proccessable array:
			col = item.split()

			# Skip 0 type lines (Comments)
			if col[0] == "0":
				continue;

			# Get the part number:
			part, ext = col[14].split('.')

			# Debug: Print the part number
			print("Part: " + part)

			# Transform the origin to the new location:
			transform[0] = float(col[5]) * float(col[2]) + float(col[6]) * float(col[3]) + float(col[7]) * float(col[4])
			transform[1] = float(col[8]) * float(col[2]) + float(col[9]) * float(col[3]) + float(col[10]) * float(col[4])
			transform[2] = float(col[11]) * float(col[2]) + float(col[12]) * float(col[3]) + float(col[13]) * float(col[4])

			# Debug: Print the new x, y, z
			print("x = " + str(transform[0]))
			print("y = " + str(transform[2]))
			print("z = " + str(-transform[1])) # z

			# Decompose the transformation matrix to get the rotation:
			rot_x = math.atan2(float(col[12]), float(col[13]))
			rot_y = math.atan2(float(col[8]), float(col[5]))
			rot_z = math.atan2(-float(col[11]), math.sqrt(float(col[12]) * float(col[12]) + float(col[13]) * float(col[13])))

			# Transform the origin to the new location in blender:
			pos_x = float(col[2]) * 0.01
			pos_y = float(col[4]) * 0.01
			if (-float(col[3])) == 24.0:
				pos_z = 0.0
			else:
				pos_z = ((-float(col[3])) - 24) * 0.01

			# Debug: Print new position and rotation:
			print("pos x = " + str(pos_x))
			print("pos y = " + str(pos_y))
			print("pos z = " + str(pos_z))

			print("rot x = " + str(int(round(math.degrees(rot_x)))))
			print("rot y = " + str(int(round(math.degrees(rot_y)))))
			print("rot z = " + str(int(round(math.degrees(rot_z)))))

			# Select the correct resolution from the import settings:
			if self.resolution == "LowRes":
				resolution = "_L"
			else:
				resolution = "_H"

			# Append the brick from the library
			filepath = library_path + "/" + part + ".blend" + "/Object/"
			directory = "/Object/"
			brick = part + resolution
			# Debug: Print the appending variables:
			print("filepath = " + filepath)
			print("directory = " + directory)
			print("filename = " + brick)
			bpy.ops.wm.append(directory=filepath, filename=brick)

			# Select the newly added brick and transform it accordingly:
			bpy.data.objects[str(part) + str(resolution)].location = (pos_x, pos_y, pos_z)
			bpy.data.objects[str(part) + str(resolution)].rotation_euler = (rot_x, rot_y, rot_z)
			bpy.data.objects[str(part) + str(resolution)].name = "Part " + str(part_num)

			# Brick Material:
			mat = bpy.data.materials.get("Material " + col[1])
			if mat is None:
				mat = bpy.data.materials.new(name=("Material " + col[1]))
				mat.use_nodes = True
				# Remove Diffuse BSDF
				mat.node_tree.nodes.remove(material.node_tree.nodes.get('Diffuse BSDF'))
				# Grab the output node:
				output_note = mat.node_tree.nodes.get('Material Output')
				# Create the Principled BSDF node:
				principled_node = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
				principled_node.inputs['Base Color'].default_value = ldraw_materials[col[1]]
				# distribution options either 'GGX' or 'MULTI_GGX'
				principled_node.distribution = 'GGX'
				principled_node.inputs['Roughness'].default_value = 0.300
				principled_node.inputs['Specular'].default_value = math.pow((1.55 - 1.00) / (1.55 + 1.0), 2) / 0.08
				mat.node_tree.links.new(output_note.inputs[0], principled_node.outputs[0])
			bpy.data.objects["Part " + str(part_num)].active_material = mat
			part_num += 1

	else:
		print("Error, file not opened!")
	ldraw_file.close()
"""
	Documentation:

	LDraw Coordinate system:

	| -y
	|
	|_______x
   /
  /
 z

	LeoCAD:
		Program coordinate system:
		| +z
		|
		|_______ +y
	   /
	  /
	 +x

	 	Test 2:
		piece at (10, 30, 24)

	Dimensions of a 1x1 brick:
		Blender:
			Brick height: 0.24
			Stud Hight: 0.04
			Brick length: 0.2
			Stud Radius: 0.06
		LDraw:
			Brick Height: 24
			Stud Height: 4
			Brick Length: 20
			Stud Radius: 6

	Brick Origins:
		3005
			B: Base of Brick (0, 0, 0)
			L: Top of brick (not stud) (0, 0, 24)
"""
