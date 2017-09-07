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

	create_materials = BoolProperty(
	name="Create Materials",
	description="Create realistic Cycles materials for the Lego bricks using Principled BSDF.",
	default=True
	)

	material_label = EnumProperty(
		name="Material names",
		description="How materials are going to be named",
		default="Code",
		items=(
			("Code", "Material XX", "Name materials by their Lego code."),
			("Col", "Color", "Name materials by their color."),
			("CodeCol", "Material XX - Color", "Name materials by code, then color."),
			("ColCode", "Color - Material XX", "Name materials by color then code.")
		)
	)

	def draw(self, context):
		layout = self.layout
		row = layout.row(align=True)
		row.prop(self, "resolution")
		row.prop(self, "linked_type")
		row.prop(self, "create_materials")
		row.prop(self, "material_label")

	def execute(self, context):
		Console.log("Future code")
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
