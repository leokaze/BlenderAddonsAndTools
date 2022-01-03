# from ntpath import join
from bpy.props import BoolProperty, StringProperty, PointerProperty
import os
import bpy

bl_info = {
    "name": "Render Output Snippets",
    "author": "leokaze",
    "version": (0, 2),
    "blender": (3, 0, 0),
    "location": "Output Properties > Render Output Snippets",
    "description": "Set output render path to varios snippets predefined",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}

def GetPath(context):
    props = context.scene.render_output_snippets_props

    fileName = (os.path.basename(bpy.data.filepath))
    dotIndex = fileName.rindex(".")
    fileName = fileName[:dotIndex]

    sceneName = bpy.context.scene.name
    layerName = bpy.context.view_layer.name
    cameraName = "NoCamera" if bpy.context.scene.camera == None else bpy.context.scene.camera.name


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
        bpy.context.scene.render.filepath = GetPath(context)
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
        col.prop(props, 'customName', text='Custom Folder')

        col = layout.column(align=True, heading="File Name to use")
        col.prop(props, 'ffileName', text='File Name')
        col.prop(props, 'fsceneName', text='Scene Name')
        col.prop(props, 'flayerName', text='Layer Name')
        col.prop(props, 'fcameraName', text='Active Camera Name')
        col.prop(props, 'fcustomName', text='Custom Name')
        col.prop(props, 'fseparatorEnd', text='Use separator at End')

        col = layout.column(align=True, heading="Custom Paths")
        # col.prop(props, 'folderPath', text='Folder path')
        col.prop(props, 'folderPath')
        col.prop(props, 'customFolder', text='Folder Name')
        col.prop(props, 'fcustomFileName', text='File Name')
        col.prop(props, 'fseparator', text='File name separator')

        col = layout.column(align=True)
        col.operator("leo_tools.render_output_snippets_operator",
                     text="Set Path")

        col = layout.column(align=True, heading="Preview path")
        col.label(text="Path: " + GetPath(context))


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
    customName:     BoolProperty(
        name="", description="Use custom folder", default=False)
    customFolder:   StringProperty(
        name="", description="folder name", default="MyFolder", maxlen=0)
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
    fcustomName:     BoolProperty(
        name="", description="Use custom file name", default=False)
    fseparatorEnd:     BoolProperty(
        name="", description="Use separator at end of file name", default=True)
    fcustomFileName:   StringProperty(
        name="", description="file name", default="MyRender", maxlen=0)
    fseparator:   StringProperty(
        name="", description="file name Separator Simbol", default="_", maxlen=0)


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
