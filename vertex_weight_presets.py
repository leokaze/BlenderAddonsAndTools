# addon to asign weight from selected vertex to vertex groups

bl_info = {
    "name": "Vertex Weight Presets",
    "description": "Assign weight from selected vertex to vertex groups",
    "author": "leokaze",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "Object Data > Vertex Weight Presets",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Tools" }

import bpy
from bpy.types import Operator, Panel
from bpy.props import FloatProperty

class AssingWeightToSelectedVertices(Operator):
    bl_idname = "object.assign_weight_to_selected_vertices"
    bl_label = "Weight Presets"
    bl_description = "Assign weight from selected vertex to vertex groups"
    bl_options = {"REGISTER", "UNDO"}

    weight: FloatProperty(name="Weight", default=1.0, min=0.0, max=1.0)

    @classmethod
    def poll(cls, context):
        return context.object and (context.object.type == 'MESH' or context.object.type == 'LATTICE')

    def execute(self, context):
        obj = context.object
        mesh = obj.data

        # get active vertex group
        active_group = obj.vertex_groups.active
        if not active_group:
            self.report({'ERROR'}, "No active vertex group")
            return {'CANCELLED'}

        # assign weight to selected vertices
        bpy.context.scene.tool_settings.vertex_group_weight = self.weight
        bpy.ops.object.vertex_group_assign()


        return {'FINISHED'}
    
class AssignWeightToSelectedVerticesPanel(Panel):
    bl_idname = "OBJECT_PT_assign_weight_to_selected_vertices"
    bl_label = "Assign Weight to Selected Vertices"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_category = 'Vertex Weight Presets'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and (obj.type == 'MESH' or obj.type == 'LATTICE') and obj.mode == 'EDIT'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.assign_weight_to_selected_vertices", text="0.0").weight = 0.0
        row.operator("object.assign_weight_to_selected_vertices", text="0.1").weight = 0.1
        row.operator("object.assign_weight_to_selected_vertices", text="0.2").weight = 0.2
        row.operator("object.assign_weight_to_selected_vertices", text="0.3").weight = 0.3
        row = layout.row()
        row.operator("object.assign_weight_to_selected_vertices", text="0.4").weight = 0.4
        row.operator("object.assign_weight_to_selected_vertices", text="0.5").weight = 0.5
        row.operator("object.assign_weight_to_selected_vertices", text="0.6").weight = 0.6
        row.operator("object.assign_weight_to_selected_vertices", text="0.7").weight = 0.7
        row = layout.row()
        row.operator("object.assign_weight_to_selected_vertices", text="0.8").weight = 0.8
        row.operator("object.assign_weight_to_selected_vertices", text="0.9").weight = 0.9
        row.operator("object.assign_weight_to_selected_vertices", text="1.0").weight = 1.0


def register():
    bpy.utils.register_class(AssingWeightToSelectedVertices)
    bpy.utils.register_class(AssignWeightToSelectedVerticesPanel)


def unregister():
    bpy.utils.unregister_class(AssingWeightToSelectedVertices)
    bpy.utils.unregister_class(AssignWeightToSelectedVerticesPanel)


if __name__ == "__main__":
    register()
    