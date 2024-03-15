import bpy

bl_info = {
  "name": "Render Format Quick Presets",
  "description": "Buttons to set render format easly",
  "author": "leokaze",
  "version": (0, 0, 3),
  "blender": (3, 0, 0),
  "location": "Output Properties > Render Format Presets",
  "warning": "This addon is still in development.",
  "wiki_url": "https://github.com/leokaze/BlenderAddonsAndTools",
  "category": "Render" }

def panel_poll_is_upper_region(region):
    # The upper region is left-aligned, the lower is split into it then.
    # Note that after "Flip Regions" it's right-aligned.
    return region.alignment in {'LEFT', 'RIGHT'}

def SetRenderFormat(formato):
  if(formato == "jpg"):
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    bpy.context.scene.render.image_settings.quality = 90
    bpy.context.scene.render.film_transparent = False
  elif(formato == "png"):
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.image_settings.color_depth = '8'
    bpy.context.scene.render.image_settings.compression = 15
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.cycles.film_transparent_glass = True
  elif(formato == "mp4"):
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
    bpy.context.scene.render.ffmpeg.gopsize = 18
    bpy.context.scene.render.film_transparent = False
  elif(formato == "exr"):
    bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.image_settings.color_depth = '32'
    bpy.context.scene.render.image_settings.exr_codec = 'ZIP'
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.cycles.film_transparent_glass = True


class RenderFormatPresetOperator(bpy.types.Operator):
  bl_idname = "set_format.render_format_presets_operator"
  bl_label = "Render Format Quick Presets"
  bl_description = "Set render format with presets"
  bl_options = {"REGISTER"}

  formato: bpy.props.StringProperty(name="formato", default="jpg")

  @classmethod
  def poll(cls, context):
    return True

  def execute(self, context):
    SetRenderFormat(self.formato)
    return {"FINISHED"}

class RenderFormatPresetsPanel(bpy.types.Panel):
  bl_idname = "RENDER_PT_render_format_quick_presets"
  bl_label = "RenderFormatQuickPresets"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "output"

  def draw(self, context):
    layout = self.layout
    layout.use_property_decorate = False
    layout.use_property_split = True

    col = layout.column(align=True, heading="Format quick presets")
    col.operator("set_format.render_format_presets_operator", text="JPEG").formato = "jpg"
    col.operator("set_format.render_format_presets_operator", text="PNG").formato = "png"
    col.operator("set_format.render_format_presets_operator", text="MP4").formato = "mp4"
    col.operator("set_format.render_format_presets_operator", text="EXR").formato = "exr"
    

def register():
  bpy.utils.register_class(RenderFormatPresetOperator)
  bpy.utils.register_class(RenderFormatPresetsPanel)

def unregister():
  bpy.utils.unregister_class(RenderFormatPresetOperator)
  bpy.utils.unregister_class(RenderFormatPresetsPanel)

if __name__ == "__main__":
  register()

