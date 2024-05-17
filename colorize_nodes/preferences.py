import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import FloatVectorProperty


def hex_to_rgb(hex_color):
    # convert hexadecimal color without # string to rgb tuple with values between 0 and 1
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))

default_colors = {
    "color_1" : {
        "hex" : "ffbe0b"
    },
    "color_2" : {
        "hex" : "fb5607"
    },
    "color_3" : {
        "hex" : "EFBDEB"
    },
    "color_4" : {
        "hex" : "8338ec"
    },
    "color_5" : {
        "hex" : "3a86ff"
    }, 
    "color_positive": {
        "hex": "2ecc71"
    },
    "color_negative": {
        "hex": "e74c3c"
    },
    "color_outputs": {
        "hex": "ff006e"
    },
    "color_inputs": {
        "hex": "ff006e"
    }
}


class ColorizeNodePreferences(AddonPreferences):
    bl_idname = __package__

    color_1: FloatVectorProperty(
        name="Color 1",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_1"]["hex"])
    ) # type: ignore
    color_2: FloatVectorProperty(
        name="Color 2",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_2"]["hex"])
    ) # type: ignore
    color_3: FloatVectorProperty(
        name ="Color 3",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_3"]["hex"])
    ) # type: ignore
    color_4: FloatVectorProperty(
        name="Color 4",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_4"]["hex"])
    ) # type: ignore
    color_5: FloatVectorProperty(
        name="Color 5",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_5"]["hex"])
    ) # type: ignore
    color_positive: FloatVectorProperty(
        name="Positive",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_positive"]["hex"])
    ) # type: ignore
    color_negative: FloatVectorProperty(
        name="Negative",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_negative"]["hex"])
    ) # type: ignore
    color_outputs: FloatVectorProperty(
        name="Outputs",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_outputs"]["hex"])
    ) # type: ignore
    color_inputs: FloatVectorProperty(
        name="Inputs",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=hex_to_rgb(default_colors["color_inputs"]["hex"])
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        for key in default_colors.keys():
            row = col.row()
            row.prop(self, key, text=key)
