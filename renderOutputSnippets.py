bl_info = {
    "name": "Render Output Snippets",
    "author": "leokaze",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Object > ",
    "description": "Set output render path to varios snippets predefined",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}

import bpy
import os
from bpy.props import BoolProperty, StringProperty, PointerProperty


class RenderOutputSnippetsOperator(bpy.types.Operator):
    """ToolTip of RenderOutputSnippetsOperator"""
    bl_idname = "addongen.render_output_snippets_operator"
    bl_label = "Render Output Snippets Operator"
    bl_options = {'REGISTER'}

    
    #@classmethod
    #def poll(cls, context):
    #    return context.object is not None

    def execute(self, context):
        props = context.scene.addongen_render_output_snippets_props
        rootPath = props.customRoot
        fileName = "NoFileName" if os.path.basename(bpy.data.filepath).split(".")[0] == "" else os.path.basename(bpy.data.filepath).split(".")[0]
        sceneName = bpy.context.scene.name
        layerName = bpy.context.view_layer.name
        cameraName = "NoCamera" if bpy.context.scene.camera == None else bpy.context.scene.camera.name
        customFolder = props.customFolder
        
        renderpath = "C:\\"
        renderpath = rootPath if props.rootPath else renderpath
        renderpath = renderpath + fileName + "\\" if props.fileName else renderpath
        renderpath = renderpath + sceneName + "\\" if props.sceneName else renderpath
        renderpath = renderpath + layerName + "\\" if props.layerName else renderpath
        renderpath = renderpath + cameraName + "\\" if props.cameraName else renderpath
        renderpath = renderpath + customFolder + "\\" if props.customName else renderpath
        
        renderpath = renderpath + fileName + props.fseparator if props.ffileName else renderpath
        renderpath = renderpath + sceneName + props.fseparator if props.fsceneName else renderpath
        renderpath = renderpath + layerName + props.fseparator if props.flayerName else renderpath
        renderpath = renderpath + cameraName + props.fseparator if props.fcameraName else renderpath
        renderpath = renderpath + props.fcustomFileName + props.fseparator if props.fcustomName else renderpath
        
        if not props.fseparatorEnd:
            renderpath = renderpath[:-len(props.fseparator)]
            
        
        bpy.context.scene.render.filepath = renderpath
        self.report({'INFO'}, "Path seted")
        return {'FINISHED'}

    #def invoke(self, context, event):
    #    wm.modal_handler_add(self)
    #    return {'RUNNING_MODAL'}
    #    return wm.invoke_porps_dialog(self)
    #def modal(self, context, event):
    #def draw(self, context):

class RenderOutputSnippetsPanel(bpy.types.Panel):
    """Docstring of RenderOutputSnippetsPanel"""
    bl_idname = "RENDER_PT_render_output_snippets"
    bl_label = "Render Output Snippets Panel"
    
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'output'

    #Panels in ImageEditor are using .poll() instead of bl_context.
    #@classmethod
    #def poll(cls, context):
    #    return context.space_data.show_paint

    def draw(self, context):
        props = context.scene.addongen_render_output_snippets_props
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        col = layout.column(align = True, heading ="Folder Path use")
        col.prop(props, 'rootPath', text='Root Path')
        col.prop(props, 'fileName', text='File Name')
        col.prop(props, 'sceneName', text='Scene Name')
        col.prop(props, 'layerName', text='Layer Name')
        col.prop(props, 'cameraName', text='Camera Name')
        col.prop(props, 'customName', text='Custom Folder')
        
        col = layout.column(align = True, heading = "File Name use")
        col.prop(props, 'ffileName', text='File Name')
        col.prop(props, 'fsceneName', text='Scene Name')
        col.prop(props, 'flayerName', text='Layer Name')
        col.prop(props, 'fcameraName', text='Camera Name')
        col.prop(props, 'fcustomName', text='Custom Name')
        col.prop(props, 'fseparatorEnd', text='Use separator at End')
        
        
        col = layout.column(align = True, heading = "Custom Paths")
        col.prop(props, 'customRoot', text='Root path')
        col.prop(props, 'customFolder', text='Folder Name')
        col.prop(props, 'fcustomFileName', text='File Name')
        col.prop(props, 'fseparator', text='Text Separator')

        col = layout.column(align = True)
        col.operator("addongen.render_output_snippets_operator", text = "Set Path")

        

class RenderOutputSnippetsProps(bpy.types.PropertyGroup):
    rootPath:     BoolProperty(name="", description="Use rootPath", default=True)
    fileName:     BoolProperty(name="", description="Actual file name", default=False)
    sceneName:     BoolProperty(name="", description="Current scene name", default=False)
    layerName:     BoolProperty(name="", description="Current Layer name", default=False)
    cameraName:     BoolProperty(name="", description="Active camera", default=False)
    customName:     BoolProperty(name="", description="Use custom folder", default=False)
    customFolder:   StringProperty(name="", description="folder name", default="MyFolder", maxlen=0)
    customRoot:   StringProperty(name="", description="Custom Root path", default="//..\\render\\", maxlen=0)
    
    ffileName:     BoolProperty(name="", description="Actual file name", default=True)
    fsceneName:     BoolProperty(name="", description="Current scene name", default=False)
    flayerName:     BoolProperty(name="", description="Current Layer name", default=False)
    fcameraName:     BoolProperty(name="", description="Active camera", default=False)
    fcustomName:     BoolProperty(name="", description="Use custom file name", default=False)
    fseparatorEnd:     BoolProperty(name="", description="Use separator at end of file name", default=False)
    fcustomFileName:   StringProperty(name="", description="file name", default="MyFile", maxlen=0)
    fseparator:   StringProperty(name="", description="file name Separator Simbol", default=" - ", maxlen=0)
    

def register():
    bpy.utils.register_class(RenderOutputSnippetsProps)
    bpy.types.Scene.addongen_render_output_snippets_props = PointerProperty(type = RenderOutputSnippetsProps)

    bpy.utils.register_class(RenderOutputSnippetsOperator)
    bpy.utils.register_class(RenderOutputSnippetsPanel)

def unregister():
    bpy.utils.unregister_class(RenderOutputSnippetsProps)
    #del bpy.types.Scene.addongen_render_output_snippets_props

    bpy.utils.unregister_class(RenderOutputSnippetsOperator)
    bpy.utils.unregister_class(RenderOutputSnippetsPanel)

if __name__ == "__main__":
    register()
