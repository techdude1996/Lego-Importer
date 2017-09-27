import os
from os import path
import math
import bpy

from . import material_lib

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
			part = part.lower()
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
			rot_z = math.atan2(float(col[11]), math.sqrt(float(col[12]) * float(col[12]) + float(col[13]) * float(col[13])))

			# Transform the origin to the new location in blender:
			pos_x = float(col[2]) * 0.01
			pos_y = float(col[4]) * 0.01
			pos_z = (-float(col[3]) * 0.01)

			# Debug: Print new position and the rotation in degrees:
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
			print("\n")
			bpy.ops.wm.append(directory=filepath, filename=brick)

			# Select brick:
			current_brick = bpy.data.objects[str(part) + str(resolution)]
			bpy.context.scene.objects.active = current_brick

			# Add the Logo to the brick studs:
			if self.logo:
				# Append the Lego Logo to the scene:
				print("Adding Logo")
				filepath = library_path + "/Logo.blend/Object/"
				directory = "/Object/"
				logo_path = "Logo.Text"
				# 0 is the Logo vertex group id
				vertex_group_id = 0
				global_verts = []
				verticies = [v for v in current_brick.data.vertices if vertex_group_id in [vg.group for vg in v.groups]]
				for vertex in verticies:
					global_verts.append(current_brick.matrix_world * vertex.co)

				for vertex in global_verts:
					# Append the logo the scene:
					bpy.ops.wm.append(directory=filepath, filename=logo_path)
					logo = bpy.data.objects["Logo.Text"]
					print(vertex[0])
					print(vertex[1])
					print(vertex[2])
					print("\n")
					logo.location = (vertex[0], vertex[1], vertex[2])
					# Select the two objects for joining:
					logo.select = True
					current_brick.select = True
					# Make the brick the active object:
					bpy.ops.object.join()

			# Select the newly added brick and transform it accordingly:
			current_brick.location = (pos_x, pos_y, pos_z)
			current_brick.rotation_euler = (rot_x, rot_y, rot_z)
			current_brick.name = 'Part ' + str(part_num)

			# Brick Material:
			if self.create_materials:
				mat = bpy.data.materials.get("Material " + col[1])
				if mat is None:
					mat = bpy.data.materials.new(name=("Material " + col[1]))
					mat.use_nodes = True
					# Remove Diffuse BSDF
					mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))
					# Grab the output node:
					output_note = mat.node_tree.nodes.get('Material Output')
					# Create the Principled BSDF node:
					principled_node = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
					principled_node.inputs['Base Color'].default_value = material_lib.ldraw_materials[col[1]]
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

	Bevel Modifier:
		Width: 0.002
		Segments: 3 for H, 1 for L

	Blender Bevel: 0.007
	units: 6 for H, 3 for L
"""
