import bpy
import random

# 查找名为 'Tiny' 的物体 source object
source_object = bpy.data.objects.get("Tiny")
# 或者 bpy.data.objects["Tiny"]

if source_object is None:
    print("没有找到名为 'Tiny' 的物体。")
else:
    # 删除现有的Tiny物体（以 "Tiny" 开头的物体），避免重复
    # do_unlink这个参数决定了删除obj物体的同时是否要与其他使用过他的地方解除关联
    for obj in bpy.data.objects:
        if obj.name.startswith("Tiny"):
            bpy.data.objects.remove(obj, do_unlink=True)

    # 定义物体的位置 xyz 3 dimension
    start_location = (0, 0, 0)
    spacing = 2  # 物体之间的间距 这里在blender中指的是2m

    for i in range(5):
        # 复制原始物体方法分三步
        # 1. copy一个新对象
        new_object = source_object.copy()
        # 2. copy origin object的网格数据(顶点 边 面)
        new_object.data = source_object.data.copy()
        # 3.将新对象link到collection中 这里link到默认集合
        bpy.context.collection.objects.link(new_object)
        
        # 设置新物体的位置 这里只偏移了x轴
        new_object.location = (start_location[0] + i * spacing, start_location[1], start_location[2])
        
        # 随机生成缩放值范围在0.5到1之间
        scale_x = random.uniform(0.5, 1.0)
        scale_y = random.uniform(0.5, 1.0)
        scale_z = random.uniform(0.5, 1.0)
        
        # 设置物体的缩放
        new_object.scale = (scale_x, scale_y, scale_z)
        
        # 重命名物体
        new_object.name = f"Tiny_{i+1}"

    print("5个Tiny物体已创建，且每个物体的缩放已随机设置。")
