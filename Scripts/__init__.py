# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info =
{
	"name": "Lego Importer",
	"author": "Ethan Snyder",
	"version": (0, 0, 1),
	"blender": (2, 79, 0),
	"location": "File > Import-Export",
	"description": "Import Lego models from either LDD (.lxf) or LDraw (.ldr/.dat) files.",
	"warning": "This plugin is still being written, expect bugs galore.",
	"wiki_url": "https://github.com/techdude1996/Lego-Importer",
	"support": 'TESTING',
	"category": "Import-Export"
}

import bpy
from bpy.props import(
		BoolProperty,
		FloatProperty,
		StringProperty,
		EmunProperty,)

class ImportLego(bpy.types.Operator):
	"""Load a Lego file (LDD/LDraw)"""
	bl_idname = "import.lego"
	bl_label = "Import Lego"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_options ={'PRESET', 'UNDO'}

	filename_ext = ".ldr"
	filer_glob = StringProperty(default="*.lxf;*.ldr;*.dat",options={'HIDDEN'})

	resolution = EnumProperty(
		name="Resolution of parts",
		description="Resolution of parts",
		default=prefs.get("resolution", "LowRes"),
		items=(
			("LowRes", "Low Resolution", "Import using low resolution parts. Great for far distance objects."),
			("HighRes", "High Resolution", "Import using high resolution parts. Great for close ups.")
		)
	)

	include_type = EnumProperty(
		name="Import type:",
		description="Link or Append the Lego parts into the current scene",
		default=prefs.get("include_type", "link"),
		items=(
			("link", "Link", "Link the parts from the library; updates scene when library changes."),
			("append", "Append", "Append the parts from the library; creates a copy of the library.")
		)
	)

	create_materials = BoolProperty(
		name="Create Materials",
		description="Create Cycles Materials for the Lego bricks using Principled BSDF.",
		default=True;
	)

def menu_func(self, context):
	self.layout.operator(ImportLego.bl_idname, text="Lego (LDD/LDraw)")

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_import.append(menuImport)

if __name__ == "__main__":
	register()
