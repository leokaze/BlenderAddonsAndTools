## All tools are created on windows and not tested on other systems.

# BlenderAddonsAndTools
In this repository I publish my addons and script tools what I create and use every day.

# Render Output Snippets

![Render Output Snippets](/PanelPreview.PNG)

This addon make easy set output path render with varios preconfigured path like name of current file and current scene.


# Render Format Quick Presets

Set the render format quick to JPG on RBG color, PNG with RBGA color, MP4 with H264 codec and EXR with Float Half color depth

# Render Batch Code Generator

Tool for save batch code in render.bat for background render. Also copy the code to clipboard if it needed. 

This addon need to be installed pyperclip module on python blender instalation.

### Install pyperclip

Search blender python folder instalation usualy in
```
C:\Program Files\Blender Foundation\Blender 3.0\3.0\python\bin
```

and then use the code
```
  python.exe -m pip install pyperclip
```

This will be all but in my case the pyperclip was be installed in windows python system folder.
To resolve this search python folder on windows system, the cmd window show were is it.
Copy the folders "pyperclip" and "pyperclip-1.8.2-py3.9.egg-info" to:
```
C:\Program Files\Blender Foundation\Blender 3.0\3.0\python\lib
```

and that's all.

Good luck.

# Dope Sheet Tools

In this section I put diferentes tools for manage keys and fcurves, this first version has the filter tool for fast filter fcurves on dope sheet and graph editor.

### Fast Filter

This tools have three icons on Dope sheet's header and Graph editor's header for fast filter 'Location', 'Rotation' and 'Scale'. Also on the right panel in the 'Tools' section there are many buttons for X, Y, Z, W Locations, Rotations and Scales filters.

# Colorize Nodes

This tool help in all node trees visualizations, fast colorize any selected node, and fast colorize all inputs and outputs nodes

![image](https://github.com/leokaze/BlenderAddonsAndTools/assets/12009166/de8ac48a-a2a2-4152-a9be-31db0a96992a)
