bl_info = {
    "name": "Set Curve Radius",
    "description": "Set curve mean radius of selected curve objects",
    "author": "leokaze",
    "version": (0, 0, 1),
    "blender": (4, 2, 1),
    "location": "N Panel > Tool > Set Curve Radius",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }

import bpy
from bpy.types import Operator, Panel

class SetCurveRadius(Operator):
    bl_idname = "object.set_curve_radius"
    bl_label = "Set Curve Radius"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        radius = 1.0
        for obj in bpy.context.selected_objects:
            if obj.type == 'CURVE':
                for spline in obj.data.splines:
                    for bPoint in spline.bezier_points:
                        bPoint.radius = radius
        return {'FINISHED'}
    
class SetCurveRadiusPanel(Panel):
    bl_label = "Set Curve Radius"
    bl_idname = "OBJECT_PT_set_curve_radius"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.set_curve_radius", text="Reset Curve Radius")

def register():
    bpy.utils.register_class(SetCurveRadius)
    bpy.utils.register_class(SetCurveRadiusPanel)

def unregister():
    bpy.utils.unregister_class(SetCurveRadius)
    bpy.utils.unregister_class(SetCurveRadiusPanel)

if __name__ == "__main__":
    register()


    