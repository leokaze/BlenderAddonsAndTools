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
from . preferences import ColorizeNodePreferences

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

def hex_to_rgb(hex_color):
    # convert hexadecimal color without # string to rgb tuple with values between 0 and 1
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

default_colors = {
    "color_1" : {
        "name" : "Amber",
        "hex" : "ffbe0b"
    },
    "color_2" : {
        "name" : "Orange (Pantone)",
        "hex" : "fb5607"
    },
    "color_3" : {
        "name" : "Rose",
        "hex" : "ff006e"
    },
    "color_4" : {
        "name" : "Blue Violet",
        "hex" : "8338ec"
    },
    "color_5" : {
        "name" : "Azure",
        "hex" : "3a86ff"
    }, 
    "color_positive": {
        "name": "Positive",
        "hex": "2ecc71"
    },
    "color_negative": {
        "name": "Negative",
        "hex": "e74c3c"
    }
}



class NodeColorsProps(PropertyGroup):
    color_1: FloatVectorProperty(
        name=default_colors["color_1"]["name"],
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_1"]["hex"])
    ) # type: ignore
    color_2: FloatVectorProperty(
        name=default_colors["color_2"]["name"],
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_2"]["hex"])
    ) # type: ignore
    color_3: FloatVectorProperty(
        name=default_colors["color_3"]["name"],
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_3"]["hex"])
    ) # type: ignore
    color_4: FloatVectorProperty(
        name=default_colors["color_4"]["name"],
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_4"]["hex"])
    ) # type: ignore
    color_5: FloatVectorProperty(
        name=default_colors["color_5"]["name"],
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_5"]["hex"])
    ) # type: ignore
    color_positive: FloatVectorProperty(
        name=default_colors["color_positive"]["name"],
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_positive"]["hex"])
    ) # type: ignore
    color_negative: FloatVectorProperty(
        name=default_colors["color_negative"]["name"],
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_negative"]["hex"])
    ) # type: ignore

class ColorizeInputAndOutputNodes(Operator):
    bl_idname = "colorize_nodes.colorize_input_output_nodes"
    bl_label = "Colorize Input and Output Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.node_colors_props
        input_color = props.color_4
        output_color = props.color_negative
        active_node = context.active_node
        if active_node is None:
            self.report({'ERROR'}, "Select any node first")
            return {'CANCELLED'}
        else:
            for node in active_node.id_data.nodes:
                if node.type == 'GROUP_OUTPUT' or node.type == 'OUTPUT_MATERIAL' or node.type == 'COMPOSITE' or node.type == 'OUTPUT_WORLD':
                    ColorizeNode(node, output_color)
                elif node.type == 'GROUP_INPUT':
                    ColorizeNode(node, input_color)

        self.report({'INFO'}, "Colorize Input and Output Nodes")
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
        props = context.scene.node_colors_props
        layout = self.layout

        col = layout.column(align=True)
        for key in default_colors.keys():
            row = col.row(align=True)
            row.prop(props, key, text="")
            row.operator("colorize_nodes.colorize_selected_nodes", text="", icon='COLOR').color = getattr(props, key)

        col = layout.column(align=True)
        col.operator("colorize_nodes.colorize_input_output_nodes", icon='COLOR')


def register():
    bpy.utils.register_class(NodeColorsProps)
    bpy.types.Scene.node_colors_props = bpy.props.PointerProperty(type=NodeColorsProps)
    bpy.utils.register_class(ColorizeInputAndOutputNodes)
    bpy.utils.register_class(ColorizeSelectedNodes)
    bpy.utils.register_class(ColorizeNodesPanel)
    bpy.utils.register_class(ColorizeNodePreferences)

def unregister():
    bpy.utils.unregister_class(NodeColorsProps)
    bpy.utils.unregister_class(ColorizeInputAndOutputNodes)
    bpy.utils.unregister_class(ColorizeSelectedNodes)
    bpy.utils.unregister_class(ColorizeNodesPanel)
    bpy.utils.unregister_class(ColorizeNodePreferences)


if __name__ == "__main__":
    register()