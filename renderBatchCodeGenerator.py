import bpy
from bpy import context
from bpy.props import BoolProperty, StringProperty, PointerProperty
import os

bl_info = {
  "name": "Render Batch Code Generator",
  "description": "Create file for render or copy de current project to batch code and send it to clipboard",
  "author": "leokaze",
  "version": (0, 0, 4),
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
    default=True
  )
  includeEnd: BoolProperty(
    name="Set end frame",
    description="Include end frame on batch code",
    default=True
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
  
def GetBatchCode(context, customProps = None):
  props = {}
  if customProps is None:
    p = context.scene.render_batch_code_generator_props
    props = {
      "renderScene": p.renderScene,
      "renderAnimation": p.renderAnimation,
      "includeOutput": p.includeOutput,
      "includeStart": p.includeStart,
      "includeEnd": p.includeEnd,
      "includeSound": p.includeSound,
      "includeShutdown": p.includeShutdown,
      "dontClose": p.dontClose,
      "appendCode": p.appendCode,
      "frames": p.frames,
      "soundPath": p.soundPath,
      "vlcPath": p.vlcPath
    }
  else:
    props = customProps

  blender = bpy.app.binary_path
  currentProyect = bpy.data.filepath
  file_name = os.path.basename(currentProyect)

  args = {
    "blender": blender,
    "background": "--background",
    "file": currentProyect,
    "render_anim": True,
    "scene": context.scene.name if customProps is None else customProps['scene_name'],
    "frame_start": context.scene.frame_start if customProps is None else customProps['frame_start'],
    "frame_end": context.scene.frame_end if customProps is None else customProps['frame_end'],
    "render_output": context.scene.render.filepath if customProps is None else customProps['file_output'],
  }

  batchCode = ""
  batchCode += "echo off\n"
  batchCode += "echo ********************************************************************************\n"
  batchCode += f"echo *************START RENDERING OF {file_name} SCENE: {args['scene']}**********\n"
  batchCode += "echo ********************************************************************************\n"
  batchCode += f"\"{args['blender']}\""
  batchCode += f" {args['background']}"
  batchCode += f" \"{args['file']}\""
  batchCode += f" --scene {args['scene']}" if props['renderScene'] else ""
  batchCode += f" --render-output \"{args['render_output']}\"" if props['includeOutput'] else ""
  batchCode += f" --frame-start {args['frame_start']}" if props['renderAnimation'] and props['includeStart'] else ""
  batchCode += f" --frame-end {args['frame_end']}" if props['renderAnimation'] and props['includeEnd'] else ""
  batchCode += f" --render-anim" if props['renderAnimation'] else f"  --render-frame {props['frames']}"
  batchCode += f" \n\"{props['vlcPath']}\" --play-and-exit \"{props['soundPath']}\"" if props['includeSound'] else ""
  batchCode += "\necho ********************************************************************************\n"
  batchCode += f"echo ********************END RENDERING OF {file_name} SCENE: {args['scene']}********************\n"
  batchCode += "echo ********************************************************************************\n"
  batchCode += f"\nshutdown /s" if props['includeShutdown'] else ""
  batchCode += f"\npause" if props['dontClose'] else ""

  return batchCode


class SaveRenderBatchFileOperator(bpy.types.Operator):
  bl_idname = "save_batch_file.save_render_batch_file_operator"
  bl_label = "Save render.bat file"
  bl_description = "Save current project to render.bat file"
  bl_options = {"REGISTER"}

  render_all: BoolProperty(
    name="Render All",
    description="Render all frames",
    default=False
  )

  @classmethod
  def poll(cls, context):
    return True

  def execute(self, context):

    # return if the file is not saved
    if not bpy.data.filepath:
      self.report({'WARNING'}, "Save your project first")
      return {"CANCELLED"}

    props = context.scene.render_batch_code_generator_props
    path = os.path.dirname(bpy.data.filepath) + "\\render.bat"

    customProps = []
    if(self.render_all):
      for scene in bpy.data.scenes:
        customProps.append({
          "renderScene": True,
          "scene_name": scene.name,
          "renderAnimation": True,
          "includeOutput": True,
          "file_output": scene.render.filepath,
          "includeStart": True,
          "frame_start": scene.frame_start,
          "includeEnd": True,
          "frame_end": scene.frame_end,
          "includeSound": props.includeSound,
          "includeShutdown": False,
          "dontClose": False,
          "appendCode": True,
          "frames": "0",
          "soundPath": props.soundPath,
          "vlcPath": props.vlcPath
        })
      with open(path, "w") as file:
        # for p in customProps:
        #   file.write(GetBatchCode(context, p))
        for p, index in zip(customProps, range(len(customProps))):
          file.write(GetBatchCode(context, p))
          if(index < len(customProps) - 1):
            file.write("\n")
          if(index == len(customProps) - 1):
            if(props.includeShutdown):
              file.write("\nshutdown /s")
            if(props.dontClose):
              file.write("\npause")
      file.close()
      self.report({'INFO'}, "All scenes in render.bat is saved")

    else:
      if(props.appendCode):
        with open(path, "a") as file:
          file.write(GetBatchCode(context))
        file.close()
      else:
        with open(path, "w") as file:
          file.write(GetBatchCode(context))
        file.close()
      self.report({'INFO'}, "render.bat is saved")
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
    col.operator("save_batch_file.save_render_batch_file_operator", text="Save render.bat").render_all = False
    col.operator("save_batch_file.save_render_batch_file_operator", text="Save all scenes").render_all = True

def register():
  bpy.utils.register_class(RenderBatchCodeProps)
  bpy.types.Scene.render_batch_code_generator_props = PointerProperty(type=RenderBatchCodeProps)
  bpy.utils.register_class(SaveRenderBatchFileOperator)
  bpy.utils.register_class(CopyBatchCodePanel)

def unregister():
  bpy.utils.unregister_class(RenderBatchCodeProps)
  bpy.utils.unregister_class(SaveRenderBatchFileOperator)
  bpy.utils.unregister_class(CopyBatchCodePanel)

if __name__ == "__main__":
  register()