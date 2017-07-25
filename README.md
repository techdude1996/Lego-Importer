# Blender Import/Export: Import Lego Model
### Blender Import Script for importing Lego models from a variety of formats.

Formats currently working on:
* Lego Digital Designer (.lxf)
* LDraw (.ldr)

## Current Brick Features:
* Import bricks with the Lego<sup>&reg;</sup> Logo. (The logo will only be placed on standard, solid studs as mapped by the LogoLoc vertex map.)
* Most bricks will be UV Unwrapped for adding Stickers/Decals (Stickers/Decals will not be included by this add-on. Importing bricks that have stickers will be imported as plain bricks.)
* High/Low Resolution for bricks
* Edge Bevel and Sharp Edges are part of the mesh for beveling and smooth shading. (The Bevel Modifier and Smooth Shading property are enabled by default)

## Disclaimer:
This importer will **NOT** be using the geometry of the bricks from the file's source program. However, these bricks are based on the geometry from LDraw. **NO DECOMPILING IS INVOLVED IN THE MAKING OF THIS ADD-ON!!!**

## Dev Notes:
* Imported files are read for instructions on where to place what brick. Documentation will eventually be put somewhere on the various formats, but a quick note: (LDD files are basic zip archives with xml instructions and a thumbnail. LDraw files are just plain text)
* Bricks are stored material-less (unless certain parts of a piece are a certain material)
* Each brick file contains both High and Low resolution models with the suffix \_H or \_L added after the brick ID. **Example: A 1x1 brick will be contained in file 3005.blend with two objects named 3005_H and 3005_L**
* Any imported brick that comes with a sticker/decal should be imported as a plain brick
