bl_info = {
	"name": "Lego Importer",
	"author": "Ethan Snyder",
	"version": (0, 0, 1),
	"blender": (2, 79, 0),
	"location": "File > Import-Export",
	"description": "Import Lego models from either LDD (.lxf) or LDraw (.ldr/.dat) files.",
	"warning": "This plugin is still being written, expect lots of bugs and crashes.",
	"wiki_url": "https://github.com/techdude1996/Lego-Importer",
	"support": 'TESTING',
	"category": "Import-Export"
}

import bpy
from bpy.props import(
		BoolProperty,
		FloatProperty,
		StringProperty,
		EnumProperty)
from bpy_extras.io_utils import (ImportHelper, path_reference_mode)

class ImportLego(bpy.types.Operator, ImportHelper):
	"""Load a Lego file (LDD/LDraw)"""
	bl_idname = "import_scene.lego"
	bl_label = "Import Lego"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_options ={'PRESET', 'UNDO', 'PRESET'}

	filename_ext = ".ldr"
	filer_glob = StringProperty(default="*.lxf;*.ldr;*.dat",options={'HIDDEN'})

	resolution = EnumProperty(
		name="Resolution of parts",
		description="Resolution of parts",
		default="LowRes",
		items=(
			("LowRes", "Low Resolution", "Import using low resolution parts. Great for far distance objects."),
			("HighRes", "High Resolution", "Import using high resolution parts. Great for close ups.")
		)
	)

	linked_type = BoolProperty(
		name="Link similar bricks",
		description="Link bricks by type and material. This links mesh data and materials, so changes to one brick changes the rest of that type and color.",
		default=True
	)

	root = BoolProperty(
		name="Add an empty",
		description="Add empty to be a master control for the entire model. Supports seperate models in single LDraw file.",
		default=True
	)

	logo = BoolProperty(
		name="Add Lego Logo",
		description="Add the Lego logo to every standard stud.",
		default=False
	)

	create_materials = BoolProperty(
	name="Create Materials",
	description="Create realistic Cycles materials for the Lego bricks using Principled BSDF.",
	default=True
	)

	bevel = BoolProperty(
		name="Add Bevel",
		description="Add the bevel modifier to all imported bricks.",
		default=True
	)

	uvmap = BoolProperty(
		name="Add UV Map",
		description="UV unwrap everybrick (if able). Most bricks can be unwrapped at any time.",
		default=False
	)

	def draw(self, context):
		layout = self.layout
		layout.label(text="Brick Resolution", icon="MOD_REMESH")
		layout.prop(self, "resolution", expand=True)
		layout.prop(self, "linked_type", icon="CONSTRAINT")
		layout.prop(self, "root", icon="OUTLINER_OB_EMPTY")
		layout.prop(self, "logo")
		layout.prop(self, "bevel", icon="MOD_BEVEL")
		layout.prop(self, "uvmap", icon="GROUP_UVS")
		layout.prop(self, "create_materials", icon="MATERIAL_DATA")

	def execute(self, context):
		# lego_file = self.filepath
		# print(lego_file)
		from . import import_lego
		import_lego.load_file(self, context)

		return {'FINISHED'}

def menuImport(self, context):
	self.layout.operator(ImportLego.bl_idname, text="Lego (LDD/LDraw)")

def register():
	bpy.utils.register_class(ImportLego)
	bpy.types.INFO_MT_file_import.append(menuImport)

def unregister():
	bpy.types.INFO_MT_file_import.remove(menuImport)
	bpy.utils.unregister_class(ImportLego)

if __name__ == "__main__":
	register()
