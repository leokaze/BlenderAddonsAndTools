import bpy
from bpy.types import Panel, Operator
from bpy.props import FloatVectorProperty
import random

def create_onions_object_collection(context):
    collection_name = "Onions"
    onions_collection = None
    if collection_name in context.scene.collection.children:
        print("Onions collection already exists")
        onions_collection = bpy.data.collections[collection_name]
        return onions_collection
    if collection_name not in bpy.data.collections:
        onions_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(onions_collection)
        print("Onions collection created")
    else:
        context.scene.collection.children.link(bpy.data.collections[collection_name])
        print("Onions collection linked")
    onions_collection = bpy.data.collections[collection_name]
    return onions_collection

def random_color_rgb(opacity=1):
    color: FloatVectorProperty = (random.random(), random.random(), random.random(), opacity)
    return color

class OnionSkinCreatorOperator(Operator):
    bl_idname = "object.onion_skin_creator"
    bl_label = "Create Onion Skin"
    bl_description = "Create Onion Skin from active object in current frame"
    bl_options = {"REGISTER"}

    def execute(self, context):
        if(context.active_object is None):
            print("No active object")
            # print information message
            self.report({'INFO'}, "No active object")
            return {"FINISHED"}
        # if object is not a mesh
        if(context.active_object.type != 'MESH'):
            print("Active object is not a mesh")
            # print information message
            self.report({'INFO'}, "Active object is not a mesh")
            return {"FINISHED"}
        onions_collection = create_onions_object_collection(context)
        active_object_name = context.active_object.name
        current_frame = context.scene.frame_current
        prefix = "Onion_f" + str(current_frame) + "_"
        # comprove if object is already an onion
        if bpy.data.objects.get(prefix + active_object_name) is not None:
            print("Object is already an onion")
            # print information message
            self.report({'INFO'}, "Object is already an onion")
            return {"FINISHED"}
        # duplicate active object
        bpy.ops.object.duplicate()
        bpy.ops.object.make_local(type='SELECT_OBDATA')
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

        # rename object
        context.active_object.name = prefix + active_object_name
        context.active_object.color = random_color_rgb(0.2)
        # add object to onions collection
        onions_collection.objects.link(context.active_object)
        # unlink object from scene collection
        context.scene.collection.objects.unlink(context.active_object)
        # delete all drivers in object
        for driver in context.active_object.animation_data.drivers:
            context.active_object.animation_data.drivers.remove(driver)
        # disable hide in render
        context.active_object.hide_render = False
        # unselect all objects
        bpy.context.object.hide_select = True
        bpy.ops.object.select_all(action='DESELECT')
        # set original object as selected
        bpy.data.objects[active_object_name].select_set(True)
        # set active object back to original
        context.view_layer.objects.active = bpy.data.objects[active_object_name]
        
        print("Onion Skin created")
        self.report({'INFO'}, "Onion Skin created")

        return {"FINISHED"}
    
class DeleteAllOnionsOperator(Operator):
    bl_idname = "object.delete_all_onions"
    bl_label = "Delete All Onions"
    bl_description = "Delete All Onions"
    bl_options = {"REGISTER"}

    def execute(self, context):
        onions_collection = create_onions_object_collection(context)
        for obj in onions_collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        # delete collection and all objects in it
        bpy.data.collections.remove(onions_collection)
        return {"FINISHED"}
    
class DeleteOnionInCurrentFrameOperator(Operator):
    bl_idname = "object.delete_onion_in_current_frame"
    bl_label = "Delete Onion objects in Current Frame"
    bl_description = "Delete Onion in Current Frame"
    bl_options = {"REGISTER"}

    def execute(self, context):
        onions_collection = create_onions_object_collection(context)
        current_frame = context.scene.frame_current
        prefix = "Onion_f" + str(current_frame) + "_"
        for objs in onions_collection.objects:
            if objs.name.startswith(prefix):
                bpy.data.objects.remove(objs, do_unlink=True)
        return {"FINISHED"}
    
class OnionSkinPanel(Panel):
    bl_idname = "ONIONSKIN_PT_onion_skin_panel"
    bl_label = "Onion Skin"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Animation"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.onion_skin_creator", text="Create Onion Skin")
        layout.operator("object.delete_all_onions", text="Delete All Onions")
        layout.operator("object.delete_onion_in_current_frame", text="Delete Onions in Current Frame")

classes = (
    OnionSkinCreatorOperator,
    OnionSkinPanel,
    DeleteAllOnionsOperator,
    DeleteOnionInCurrentFrameOperator
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()