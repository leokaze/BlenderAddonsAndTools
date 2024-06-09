# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import Panel, Operator, PropertyGroup, AddonPreferences
from bpy.props import FloatVectorProperty
from . preferences import ColorizeNodePreferences, DEFAULT_COLORS, ColorizeNodesResetDefaultColorsOp

bl_info = {
    "name" : "Colorize Nodes",
    "author" : "leokaze",
    "description" : "",
    "blender" : (4, 1, 1),
    "version" : (0, 0, 1),
    "location" : "Node Editor > Sidebar > Node",
    "warning" : "",
    "category" : "Node"
}


def ColorizeNode(node, color):
    node.use_custom_color = True
    node.color = color

class ColorizeResetColor(Operator):
    bl_idname = "colorize_nodes.reset_color"
    bl_label = "Reset Colors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_node = context.active_node
        if active_node is None:
            self.report({'ERROR'}, "No node selected")
            return {'CANCELLED'}
        else:
            for node in context.selected_nodes:
                node.color = (0.608, 0.608, 0.608)
                node.use_custom_color = False

        self.report({'INFO'}, "Reset Color")
        return {'FINISHED'}

class ColorizeInputAndOutputNodes(Operator):
    bl_idname = "colorize_nodes.colorize_input_output_nodes"
    bl_label = "Colorize Input and Output Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        color_preferences = preferences.addons[__package__].preferences
        active_node = context.active_node
        if active_node is None:
            self.report({'ERROR'}, "Select any node first")
            return {'CANCELLED'}
        else:
            for node in active_node.id_data.nodes:
                if node.type == 'GROUP_OUTPUT' or node.type == 'OUTPUT_MATERIAL' or node.type == 'COMPOSITE' or node.type == 'OUTPUT_WORLD':
                    ColorizeNode(node, color_preferences.color_outputs)
                elif node.type == 'GROUP_INPUT':
                    ColorizeNode(node, color_preferences.color_inputs)

        self.report({'INFO'}, "Colorize Input and Output Nodes")
        return {'FINISHED'}
    
class HideUnusedSocketsOfInputNodes(Operator):
    bl_idname = "colorize_nodes.hide_unused_sockets_of_input_nodes"
    bl_label = "Hide Unused Sockets of Input Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_node = context.active_node
        if active_node is None:
            self.report({'ERROR'}, "Select any node first")
            return {'CANCELLED'}
        else:
            for node in active_node.id_data.nodes:
                if node.type == 'GROUP_INPUT':
                    for socket in node.outputs:
                        socket.hide = True

        self.report({'INFO'}, "Hide Unused Sockets of Input Nodes")
        return {'FINISHED'}
    
class ColorizeSelectedNodes(Operator):
    bl_idname = "colorize_nodes.colorize_selected_nodes"
    bl_label = "Colorize Selected Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=(1.0, 0.0, 0.0)
    ) # type: ignore

    def execute(self, context):
        active_node = context.active_node
        color = self.color
        print(color)
        if active_node is None:
            self.report({'ERROR'}, "No node selected")
            return {'CANCELLED'}
        else:
            for node in context.selected_nodes:
                ColorizeNode(node, color)

        self.report({'INFO'}, "Colorize Selected Nodes")
        return {'FINISHED'}

class ColorizeNodesPanel(Panel):
    bl_idname = "COLOR_PT_colorize_nodes"
    bl_label = "Colorize Nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node'

    def draw(self, context):
        preferences = context.preferences
        color_preferences = preferences.addons[__package__].preferences

        layout = self.layout

        col = layout.column(align=True)
        for key in DEFAULT_COLORS.keys():
            row = col.row(align=True)
            # row.prop(props, key, text="")
            # row.operator("colorize_nodes.colorize_selected_nodes", text="", icon='COLOR').color = getattr(props, key)
            row.prop(color_preferences, key, text="")
            row.operator("colorize_nodes.colorize_selected_nodes", text="", icon='COLOR').color = getattr(color_preferences, key)

        col = layout.column(align=True)
        col.operator("colorize_nodes.colorize_input_output_nodes", icon='COLOR', text="Colorize Input and Output")
        col.operator("colorize_nodes.reset_color", icon='X')
        col.operator("colorize_nodes.hide_unused_sockets_of_input_nodes", icon='HIDE_OFF', text="Hide Inputs Sockets")


def register():
    bpy.utils.register_class(ColorizeInputAndOutputNodes)
    bpy.utils.register_class(ColorizeResetColor)
    bpy.utils.register_class(ColorizeNodesResetDefaultColorsOp)
    bpy.utils.register_class(ColorizeSelectedNodes)
    bpy.utils.register_class(ColorizeNodesPanel)
    bpy.utils.register_class(ColorizeNodePreferences)
    bpy.utils.register_class(HideUnusedSocketsOfInputNodes)

def unregister():
    bpy.utils.unregister_class(ColorizeInputAndOutputNodes)
    bpy.utils.unregister_class(ColorizeResetColor)
    bpy.utils.unregister_class(ColorizeNodesResetDefaultColorsOp)
    bpy.utils.unregister_class(ColorizeSelectedNodes)
    bpy.utils.unregister_class(ColorizeNodesPanel)
    bpy.utils.unregister_class(ColorizeNodePreferences)
    bpy.utils.unregister_class(HideUnusedSocketsOfInputNodes)


if __name__ == "__main__":
    register()