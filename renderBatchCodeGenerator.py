import bpy
from bpy import context
from bpy.props import BoolProperty, StringProperty, PointerProperty
import os

bl_info = {
  "name": "Render Batch Code Generator",
  "description": "Create file for render or copy de current project to batch code and send it to clipboard",
  "author": "leokaze",
  "version": (0, 0, 3),
  "blender": (3, 0, 0),
  "location": "Output Properties > Batch Code",
  "warning": "This addon is still in development. Is needed install pyperclip on on current blender python folder",
  "wiki_url": "https://github.com/leokaze/BlenderAddonsAndTools",
  "category": "Render" }

class RenderBatchCodeProps(bpy.types.PropertyGroup):
  renderScene: BoolProperty(
    name="Scene name",
    description="Include current scene to batch code",
    default=False
  )
  renderAnimation: BoolProperty(
    name="Render Animation",
    description="Include animation code to render batch code",
    default=True
  )
  includeOutput: BoolProperty(
    name="Output path",
    description="Use current output path seted",
    default=False
  )
  includeStart: BoolProperty(
    name="Set start frame",
    description="Include start frame on code",
    default=False
  )
  includeEnd: BoolProperty(
    name="Set end frame",
    description="Include end frame on batch code",
    default=False
  )
  includeSound: BoolProperty(
    name="Use sound",
    description="Use soun at end of render",
    default=False
  )
  includeShutdown: BoolProperty(
    name="Shutdown PC",
    description="Shutdown PC at render end",
    default=False
  )
  dontClose: BoolProperty(
    name="Dont close window",
    description="Dont close cmd window at end of render",
    default=True
  )
  appendCode: BoolProperty(
    name="Append code",
    description="Append the new code to existing render.bat file",
    default=True
  )
  startFrame: StringProperty(
    name="Start frame",
    description="Start frame to render",
    default="1"
  )
  endFrame: StringProperty(
    name="End frame",
    description="Set de end frame to render",
    default="250"
  )
  frames: StringProperty(
    name="Frames to render",
    description="Set the frames to render if animation is not seted, separated by commas(no spaces). User .. to range frames",
    default="0"
  )
  soundPath: StringProperty(
    name="Sound Path",
    description="Search sound path to use. This use vlc for play sound",
    default="D:\MisDocumentos\Musica\sound.wav",
    subtype="FILE_PATH",
    maxlen=1024
  )
  vlcPath: StringProperty(
    name="VLC.exe Path",
    description="Use vlc for play sound",
    default="C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    subtype="FILE_PATH",
    maxlen=1024,
  )
  
def GetBatchCode(context):
  props = context.scene.render_batch_code_generator_props

  blender = bpy.app.binary_path
  currentProyect = bpy.data.filepath

  batchCode = "\"" + blender + "\" --background \"" + currentProyect + "\""
  if(props.includeOutput):
    batchCode += " --render-output \"" + bpy.context.scene.render.filepath + "\""
  if(props.renderScene):
    batchCode += " --scene \"" + bpy.context.scene.name + "\""
  if(props.renderAnimation):
    if(props.includeStart):
      batchCode += " --frame-start " + props.startFrame
    if(props.includeEnd):
      batchCode += " --frame-end " + props.endFrame
    batchCode += " --render-anim"
  else:
    batchCode += " --render-frame " + props.frames

  if(props.includeSound):
    batchCode += "\n\"" + props.vlcPath + "\" --play-and-exit \"" + props.soundPath + "\""

  if(props.includeShutdown):
    batchCode += "\n\nshutdown \\s"

  if(props.dontClose):
    batchCode += "\n\npause"

  batchCode += "\n\n---------------------------------------\n\n"


  print(batchCode)
  return batchCode

class CopyProjectBatchCodeOperator(bpy.types.Operator):
  bl_idname = "copy_batch.copy_project_batch_code_operator"
  bl_label = "Copy Batch Code"
  bl_description = "Send to clipboard de current projecto on batch code"
  bl_options = {"REGISTER"}

  @classmethod
  def poll(cls, context):
    return True

  def execute(self, context):
    code = GetBatchCode(context)
    self.report({'INFO'}, "No longer available!")
    return {"FINISHED"}

class SaveRenderBatchFileOperator(bpy.types.Operator):
  bl_idname = "save_batch_file.save_render_batch_file_operator"
  bl_label = "Save render.bat file"
  bl_description = "Save current project to render.bat file"
  bl_options = {"REGISTER"}

  @classmethod
  def poll(cls, context):
    return True

  def execute(self, context):
    props = context.scene.render_batch_code_generator_props
    path = "NOT_SAVED!!!"
    if(len(bpy.data.filepath) > 3):
      path = os.path.dirname(bpy.data.filepath) + "\\render.bat"
      if(props.appendCode):
        with open(path, "a") as file:
          file.write(GetBatchCode(context))
        file.close()
      else:
        with open(path, "w") as file:
          file.write(GetBatchCode(context))
        file.close()
      self.report({'INFO'}, "render.bat is saved")
    else:
      self.report({'WARNING'}, "Current proyect is not saved!!!")
    # print(path)
    return {"FINISHED"}

class CopyBatchCodePanel(bpy.types.Panel):
  bl_idname = "RENDER_PT_copy_batch_code_render"
  bl_label = "Render Batch Code Generator"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "output"

  def draw(self, context):
    props = context.scene.render_batch_code_generator_props
    layout = self.layout
    layout.use_property_decorate = False
    layout.use_property_split = True

    col = layout.column(align=True, heading="Include")
    col.prop(props, "includeOutput")
    col.prop(props, "renderScene")
    col.prop(props, "renderAnimation")
    col.prop(props, "includeStart")
    col.prop(props, "includeEnd")

    row = layout.row()
    row.prop(props, "startFrame")
    row.prop(props, "endFrame")

    col = layout.column()
    col.prop(props, "frames")

    col = layout.column(align=True, heading="Extras")
    col.prop(props, "dontClose")
    col.prop(props, "includeShutdown")
    col.prop(props, "includeSound")
    col.prop(props, "vlcPath")
    col.prop(props, "soundPath")
    
    col = layout.column()
    col.prop(props, "appendCode")
    col.operator("copy_batch.copy_project_batch_code_operator", text="Copy to clipboard")
    col.operator("save_batch_file.save_render_batch_file_operator", text="Save render.bat")

def register():
  bpy.utils.register_class(RenderBatchCodeProps)
  bpy.types.Scene.render_batch_code_generator_props = PointerProperty(type=RenderBatchCodeProps)
  bpy.utils.register_class(CopyProjectBatchCodeOperator)
  bpy.utils.register_class(SaveRenderBatchFileOperator)
  bpy.utils.register_class(CopyBatchCodePanel)

def unregister():
  bpy.utils.unregister_class(RenderBatchCodeProps)
  bpy.utils.unregister_class(CopyProjectBatchCodeOperator)
  bpy.utils.unregister_class(SaveRenderBatchFileOperator)
  bpy.utils.unregister_class(CopyBatchCodePanel)

if __name__ == "__main__":
  register()