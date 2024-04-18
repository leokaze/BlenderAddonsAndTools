# from ntpath import join
from bpy.props import BoolProperty, StringProperty, PointerProperty
import os
import bpy

bl_info = {
    "name": "Render Output Snippets",
    "author": "leokaze",
    "version": (0, 4),
    "blender": (3, 0, 0),
    "location": "Output Properties > Render Output Snippets",
    "description": "Set output render path to varios snippets predefined",
    "warning": "",
    "wiki_url": "https://github.com/leokaze/BlenderAddonsAndTools",
    "tracker_url": "",
    "category": "Render"}

def GetFileName():
    fileName = (os.path.basename(bpy.data.filepath))
    try:
        dotIndex = fileName.rindex(".")
    except:
        return "Project-Unsaved"
    fileName = fileName[:dotIndex]
    # replaces underscores with - to avoid problems with the file name
    fileName = fileName.replace("_", "-")
    return fileName

def GetPath(context):
    props = context.scene.render_output_snippets_props

    fileName = (os.path.basename(bpy.data.filepath))
    try:
        dotIndex = fileName.rindex(".")
    except:
        return "//..\\SaveYourProjectFirst\\"
    fileName = fileName[:dotIndex]

    sceneName = bpy.context.scene.name
    layerName = bpy.context.view_layer.name
    cameraName = "NoCamera" if bpy.context.scene.camera == None else bpy.context.scene.camera.name
    activeCollectionName = bpy.context.view_layer.active_layer_collection.name


    renderPath = props.folderPath
    if(renderPath[-1] == "\\"):
        renderPath = renderPath[:-1]
    renderName = ""

    if(props.fileName):
        renderPath += "\\" + fileName
    if(props.sceneName):
        renderPath += "\\" + sceneName
    if(props.layerName):
        renderPath += "\\" + layerName
    if(props.cameraName):
        renderPath += "\\" + cameraName
    if(props.collectionName):
        renderPath += "\\" + activeCollectionName
    if(props.customName):
        renderPath += "\\" + props.customFolder

    if(props.ffileName):
        renderName = fileName
    if(props.fsceneName):
        renderName += sceneName if len(renderName) == 0 else props.fseparator + sceneName
    if(props.flayerName):
        renderName += layerName if len(renderName) == 0 else props.fseparator + layerName
    if(props.fcameraName):
        renderName += cameraName if len(renderName) == 0 else props.fseparator + cameraName
    if(props.fcollectionName):
        renderName += activeCollectionName if len(renderName) == 0 else props.fseparator + activeCollectionName
    if(props.fcustomName):
        renderName += props.fcustomFileName if len(renderName) == 0 else props.fseparator + props.fcustomFileName
    if(props.fseparatorEnd):
        renderName += props.fseparator

    if(len(renderPath) == 0):
        renderPath = "//"
    if(len(renderName) == 0):
        renderName = "MyRender"

    return renderPath + "\\" + renderName

class RenderOutputSnippetsOperator(bpy.types.Operator):
    """ToolTip of RenderOutputSnippetsOperator"""
    bl_idname = "leo_tools.render_output_snippets_operator"
    bl_label = "Render Output Snippets Operator"
    bl_options = {'REGISTER'}

    def execute(self, context):
        props = context.scene.render_output_snippets_props
        bpy.context.scene.render.filepath = GetPath(context)

        if(props.viewMetadata):
            context.scene.render.use_stamp_date = False
            context.scene.render.use_stamp_time = False
            context.scene.render.use_stamp_render_time = False
            context.scene.render.use_stamp_frame = True
            context.scene.render.use_stamp_frame_range = False
            context.scene.render.use_stamp_memory = False
            context.scene.render.use_stamp_hostname = False
            context.scene.render.use_stamp_camera = True
            context.scene.render.use_stamp_lens = False

            if(len(bpy.data.scenes) > 1):
                context.scene.render.use_stamp_scene = True
            else:
                context.scene.render.use_stamp_scene = False

            context.scene.render.use_stamp_marker = False
            context.scene.render.use_stamp_filename = False
            context.scene.render.use_stamp_sequencer_strip = False
            context.scene.render.use_stamp_note = True
            context.scene.render.stamp_note_text = GetFileName()
            context.scene.render.use_stamp = True
            context.scene.render.stamp_font_size = 30
            context.scene.render.stamp_foreground = (1, 1, 1, 1)
            context.scene.render.stamp_background = (0, 0, 0, 0.8)
        else:
            context.scene.render.use_stamp = False

        self.report({'INFO'}, "Path seted")
        return {'FINISHED'}


class RenderOutputSnippetsPanel(bpy.types.Panel):
    """Docstring of RenderOutputSnippetsPanel"""
    bl_idname = "RENDER_PT_render_output_snippets"
    bl_label = "Render Output Snippets"

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'output'

    def draw(self, context):
        props = context.scene.render_output_snippets_props
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        col = layout.column(align=True, heading="Folder Path to use")
        # col.prop(props, 'rootPath', text='Root Path')
        col.prop(props, 'fileName', text='File Name')
        col.prop(props, 'sceneName', text='Scene Name')
        col.prop(props, 'layerName', text='Layer Name')
        col.prop(props, 'cameraName', text='Active Camera Name')
        col.prop(props, 'collectionName', text='Active Collection Name')
        col.prop(props, 'customName', text='Custom Folder')

        col = layout.column(align=True, heading="File Name to use")
        col.prop(props, 'ffileName', text='File Name')
        col.prop(props, 'fsceneName', text='Scene Name')
        col.prop(props, 'flayerName', text='Layer Name')
        col.prop(props, 'fcameraName', text='Active Camera Name')
        col.prop(props, 'fcustomName', text='Custom Name')
        col.prop(props, 'fcollectionName', text='Active Collection Name')
        col.prop(props, 'fseparatorEnd', text='Use separator at End')

        col = layout.column(align=True, heading="Custom Paths")
        # col.prop(props, 'folderPath', text='Folder path')
        col.prop(props, 'folderPath')
        col.prop(props, 'customFolder', text='Folder Name')
        col.prop(props, 'fcustomFileName', text='File Name')
        col.prop(props, 'fseparator', text='File name separator')

        col = layout.column(align=True, heading="View Metadata")
        col.prop(props, 'viewMetadata', text='')

        col = layout.column(align=True)
        col.operator("leo_tools.render_output_snippets_operator",
                     text="Set Path")

        col = layout.column(align=True, heading="Preview path")
        col.label(text="PREVIEW")
        col.label(text="- " + GetPath(context))

        col = layout.column(align=True, heading="Current path")
        col.label(text="CURRENT")
        col.label(text="- " + bpy.context.scene.render.filepath)




class RenderOutputSnippetsProps(bpy.types.PropertyGroup):
    rootPath:     BoolProperty(
        name="", description="Use rootPath", default=True)
    fileName:     BoolProperty(
        name="", description="Actual file name", default=True)
    sceneName:     BoolProperty(
        name="", description="Current scene name", default=False)
    layerName:     BoolProperty(
        name="", description="Current Layer name", default=False)
    cameraName:     BoolProperty(
        name="", description="Active camera", default=False)
    collectionName:     BoolProperty(
        name="", description="Active Collection", default=False)
    customName:     BoolProperty(
        name="", description="Use custom folder", default=False)
    customFolder:   StringProperty(
        name="", description="folder name", default="Preview", maxlen=0)
    folderPath:   StringProperty(
        name="Folder Path", description="Custom folder path", default="//..\\render\\", maxlen=1024, subtype="DIR_PATH")

    ffileName:     BoolProperty(
        name="", description="Actual file name", default=True)
    fsceneName:     BoolProperty(
        name="", description="Current scene name", default=False)
    flayerName:     BoolProperty(
        name="", description="Current Layer name", default=False)
    fcameraName:     BoolProperty(
        name="", description="Active camera", default=False)
    fcollectionName:     BoolProperty(
        name="", description="Active Collection", default=False)
    fcustomName:     BoolProperty(
        name="", description="Use custom file name", default=False)
    fseparatorEnd:     BoolProperty(
        name="", description="Use separator at end of file name", default=True)
    fcustomFileName:   StringProperty(
        name="", description="file name", default="Preview", maxlen=0)
    fseparator:   StringProperty(
        name="", description="file name Separator Simbol", default="_", maxlen=0)
    
    viewMetadata:  BoolProperty(
        name="", description="View Metadata", default=False)


def register():
    bpy.utils.register_class(RenderOutputSnippetsProps)
    bpy.types.Scene.render_output_snippets_props = PointerProperty(
        type=RenderOutputSnippetsProps)

    bpy.utils.register_class(RenderOutputSnippetsOperator)
    bpy.utils.register_class(RenderOutputSnippetsPanel)


def unregister():
    bpy.utils.unregister_class(RenderOutputSnippetsProps)

    bpy.utils.unregister_class(RenderOutputSnippetsOperator)
    bpy.utils.unregister_class(RenderOutputSnippetsPanel)


if __name__ == "__main__":
    register()
