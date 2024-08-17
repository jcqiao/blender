# blender

## Model

1. bpy

    `bpy` 是 Blender 的 Python API 模块，它提供了一整套工具，用于在 Blender 中通过脚本自动化任务、创建或修改 3D 模型、场景设置、动画、渲染等各种操作。
    ### 主要功能
    · 场景管理：可以通过 bpy 操作 Blender 场景中的各个元素，如对象、灯光、摄像机等。
    · 创建与编辑模型：可以使用 bpy 创建新的几何形状、修改已有模型的顶点、边和面。
    ### 常用属性
    1. `bpy.data`提供了对 Blender 中所有数据块（如对象、网格、材质、灯光等）的全局访问。
    · bpy.data.objects: 场景中的所有对象。
    · bpy.data.meshes: 所有的网格数据。
    · bpy.data.materials: 所有的材质。
    · bpy.data.textures: 所有的纹理。
    · bpy.data.cameras: 所有的摄像机。
    · bpy.data.lights: 所有的灯光。
    · bpy.data.scenes: 所有的场景。
    · bpy.data.collections: 所有的集合。
    2. `bpy.context`提供了对当前 Blender 上下文的访问，包括当前场景、所选对象、活动模式等。
    · bpy.context.scene: 当前活动的场景。
    · bpy.context.object: 当前活动的对象。
    · bpy.context.selected_objects: 当前选中的所有对象。
    · bpy.context.view_layer: 当前的视图层。
    · bpy.context.mode: 当前模式（如对象模式、编辑模式等）。 
    · bpy.context.collection: 当前场景的根合集

2.  `mathutils`
     `mathutils`是 Blender 中用于数学和几何计算的 Python 模块，它提供了一些用于处理向量、矩阵、四元数和其他数学对象的类和函数。mathutils 是 Blender API 的一部分，旨在帮助开发人员和艺术家在脚本和插件中进行复杂的数学运算和几何变换。
     ### 主要组件
    1. Vector:
    用途: 表示三维或二维向量。用于处理位置、方向、速度等。
    常用方法:
    · length(): 计算向量的长度（模）。
    · normalize(): 归一化向量，使其长度为 1。
    · dot(vector): 计算两个向量的点积。
    ·cross(vector): 计算两个向量的叉积。
    2. Matrix:
    用途: 表示 2D 或 3D 转换矩阵。用于处理缩放、旋转、平移等变换。
    常用方法:
    · translation: 创建平移矩阵。
    · rotation: 创建旋转矩阵。
    · scale: 创建缩放矩阵。
    · inverted(): 计算矩阵的逆。
    3. Quaternion:
    用途: 表示四元数，用于旋转操作。四元数避免了欧拉角的万向节锁问题。
    常用方法:
    · to_euler(): 转换为欧拉角。
    · to_matrix(): 转换为旋转矩阵。
    · slerp(quaternion, factor): 在两个四元数之间进行球面线性插值。
    4. Color:
    用途: 表示颜色。支持 RGB 和 HSV 色彩模式。
    常用方法:
    · hsv: 从 HSV 颜色空间创建颜色。
    · rgb: 从 RGB 颜色空间创建颜色。

