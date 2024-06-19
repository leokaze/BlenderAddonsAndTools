bl_info = {
    "name": "Copy Objects Names to Data",
    "description": "Copy the names of the objects to the data names of the selected objects.",
    "author": "leokaze",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "Object Data > Copy Objects Names to Data",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Tools" }
    

import bpy
from bpy.types import Operator, Panel


class OBJECT_OT_copy_objects_names_to_data(Operator):
    bl_idname = "object.copy_objects_names_to_data"
    bl_label = "Copy Objects Names to Data"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in context.selected_objects:
            obj.data.name = obj.name
        return {'FINISHED'}
    

class OBJECT_PT_copy_objects_names_to_data(Panel):
    bl_idname = "OBJECT_PT_copy_objects_names_to_data"
    bl_label = "Copy Objects Names to Data"
    # place in object data panel
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    # class method to disable on EMPTY objects
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type != 'EMPTY'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.copy_objects_names_to_data")


def register():
    bpy.utils.register_class(OBJECT_OT_copy_objects_names_to_data)
    bpy.utils.register_class(OBJECT_PT_copy_objects_names_to_data)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_copy_objects_names_to_data)
    bpy.utils.unregister_class(OBJECT_PT_copy_objects_names_to_data)


if __name__ == "__main__":
    register()