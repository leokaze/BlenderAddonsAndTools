import bpy

bl_info = {
  "name": "Dope Sheet Tools",
  "description": "Tools to manipulate filters and fcurves",
  "author": "leokaze",
  "version": (0, 0, 2),
  "blender": (3, 0, 0),
  "location": "Dope Sheet and Graph Editor",
  "warning": "This addon is still in development.",
  "wiki_url": "",
  "category": "Animation" }
  
class FastFilterFCurvesOP(bpy.types.Operator):
  bl_idname = "fastfilter.fcurves_filter"
  bl_label = "Fast Filter Fcurves"
  bl_description = "Tool for fast filter on fcurves"
  bl_options = {"REGISTER"}

  filtro: bpy.props.StringProperty(name="filtro", default="")

  @classmethod
  def poll(cls, context):
    return True

  def execute(self, context):
    bpy.context.space_data.dopesheet.filter_text = self.filtro
    return {"FINISHED"}

class FrameJumpsOP(bpy.types.Operator):
  bl_idname = "framejumps.animation_tools"
  bl_label = "Frame Jumps"
  bl_description = "Various frame jumps most used in animation."
  bl_options = {"REGISTER"}

  jump: bpy.props.IntProperty(name="jump", default=9)

  @classmethod
  def poll(cls, context):
    return True

  def execute(self, context):
    jump = self.jump
    if(jump > 0):
      jump = bpy.context.scene.frame_current + jump - 1
    else:
      jump = bpy.context.scene.frame_current + jump + 1
    bpy.context.scene.frame_set(jump)
    return {"FINISHED"}


class PanelDopesheetFastFilterFcurves(bpy.types.Panel):
  bl_idname = "FASTFILTER_PT_dopesheet_panel"
  bl_label = "Fast Filter"
  bl_space_type = "DOPESHEET_EDITOR"
  bl_region_type = "UI"
  bl_category = "Tools"

  def draw(self, context):
    layout = self.layout

    layout.use_property_decorate = False
    layout.use_property_split = True

    row = layout.row(align=True, heading="Location")
    row.label(text="Location")
    row = layout.row(align=True, heading="Location")
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Location"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Location"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Location"

    row = layout.row(align=True, heading="Quaternion")
    row.label(text="Quaternion")
    row = layout.row(align=True, heading="Quaternion")
    row.operator("fastfilter.fcurves_filter", text="W").filtro = "W Quaternion Rotation"
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Quaternion Rotation"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Quaternion Rotation"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Quaternion Rotation"

    row = layout.row(align=True, heading="Euler")
    row.label(text="Euler")
    row = layout.row(align=True, heading="Euler")
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Euler"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Euler"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Euler"

    row = layout.row(align=True, heading="Scale")
    row.label(text="Scale")
    row = layout.row(align=True, heading="Scale")
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Scale"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Scale"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Scale"
    

class PanelDopesheetFrameJump(bpy.types.Panel):
  bl_idname = "FRAMEJUMPS_PT_dopesheet_panel"
  bl_label = "Frame jumps"
  bl_space_type = "DOPESHEET_EDITOR"
  bl_region_type = "UI"
  bl_category = "Tools"

  def draw(self, context):
    layout = self.layout

    layout.use_property_decorate = False
    layout.use_property_split = True

    row = layout.row(align=True)
    row.operator("framejumps.animation_tools", text="-3").jump = -3
    row.operator("framejumps.animation_tools", text="+3").jump = 3

    row = layout.row(align=True)
    row.operator("framejumps.animation_tools", text="-5").jump = -5
    row.operator("framejumps.animation_tools", text="+5").jump = 5

    row = layout.row(align=True)
    row.operator("framejumps.animation_tools", text="-7").jump = -7
    row.operator("framejumps.animation_tools", text="+7").jump = 7

    row = layout.row(align=True)
    row.operator("framejumps.animation_tools", text="-9").jump = -9
    row.operator("framejumps.animation_tools", text="+9").jump = 9

    row = layout.row(align=True)
    row.operator("framejumps.animation_tools", text="-11").jump = -11
    row.operator("framejumps.animation_tools", text="+11").jump = 11

    row = layout.row(align=True)
    row.operator("framejumps.animation_tools", text="-13").jump = -13
    row.operator("framejumps.animation_tools", text="+13").jump = 13
    

class PanelGraphFastFilterFcurves(bpy.types.Panel):
  bl_idname = "FASTFILTER_PT_graph_panel"
  bl_label = "Fast Filter"
  bl_space_type = "GRAPH_EDITOR"
  bl_region_type = "UI"
  bl_category = "Tools"

  def draw(self, context):
    layout = self.layout

    layout.use_property_decorate = False
    layout.use_property_split = True

    row = layout.row(align=True, heading="Location")
    row.label(text="Location")
    row = layout.row(align=True, heading="Location")
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Location"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Location"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Location"

    row = layout.row(align=True, heading="Quaternion")
    row.label(text="Quaternion")
    row = layout.row(align=True, heading="Quaternion")
    row.operator("fastfilter.fcurves_filter", text="W").filtro = "W Quaternion Rotation"
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Quaternion Rotation"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Quaternion Rotation"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Quaternion Rotation"

    row = layout.row(align=True, heading="Euler")
    row.label(text="Euler")
    row = layout.row(align=True, heading="Euler")
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Euler"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Euler"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Euler"

    row = layout.row(align=True, heading="Scale")
    row.label(text="Scale")
    row = layout.row(align=True, heading="Scale")
    row.operator("fastfilter.fcurves_filter", text="X").filtro = "X Scale"
    row.operator("fastfilter.fcurves_filter", text="Y").filtro = "Y Scale"
    row.operator("fastfilter.fcurves_filter", text="Z").filtro = "Z Scale"
    

def menu_func(self, context):
  row = self.layout.row(align=True)
  row.operator("fastfilter.fcurves_filter", text="", icon="ORIENTATION_GLOBAL").filtro = "Location"
  row.operator("fastfilter.fcurves_filter", text="", icon="ORIENTATION_GIMBAL").filtro = "Rotation"
  row.operator("fastfilter.fcurves_filter", text="", icon="CON_SIZELIKE").filtro = "Scale"


def register():
  bpy.utils.register_class(FastFilterFCurvesOP)
  bpy.utils.register_class(PanelDopesheetFastFilterFcurves)
  bpy.utils.register_class(PanelGraphFastFilterFcurves)
  bpy.utils.register_class(FrameJumpsOP)
  bpy.utils.register_class(PanelDopesheetFrameJump)
  bpy.types.DOPESHEET_HT_header.append(menu_func)
  bpy.types.GRAPH_HT_header.append(menu_func)

def unregister():
  bpy.utils.unregister_class(FastFilterFCurvesOP)
  bpy.utils.unregister_class(PanelDopesheetFastFilterFcurves)
  bpy.utils.unregister_class(PanelGraphFastFilterFcurves)
  bpy.utils.unregister_class(FrameJumpsOP)
  bpy.utils.unregister_class(PanelDopesheetFrameJump)
  bpy.types.DOPESHEET_HT_header.remove(menu_func)
  bpy.types.GRAPH_HT_header.remove(menu_func)

if __name__ == "__main__":
  register()
