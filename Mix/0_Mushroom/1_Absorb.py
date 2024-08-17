# 在createObject基础上实现吸附功能
import bpy
import random
import mathutils

# define a funtion named is_exterior_face 是否是外法相
# 用来区分内外方向
# 目的是想物体只吸附在外面表面 而不是内侧表面，face是面 obj是target object
def is_exterior_face(face, obj):
    # 计算面法线
    # obj.matrix_world:
    # 是一个 4x4 的变换矩阵，它表示对象 obj 在世界坐标系中的位置、旋转和缩放。这个矩阵将对象的局部坐标系转换到世界坐标系。
    # obj.matrix_world.to_3x3() 将 4x4 的变换矩阵转换为 3x3 的矩阵。4x4 矩阵中包含了平移分量，而 3x3 矩阵只包含旋转和缩放分量。
    # 在 3D 图形中，法线向量的旋转和缩放变换通常只涉及到 3x3 部分，因为平移分量对法线向量的变换没有影响。
    # face.normal:
    # face.normal 是面 face 的法线向量，它通常是在对象的局部坐标系中定义的。
    # @ 运算符:在 Blender 的 Python API 中，@ 是矩阵和向量之间的乘法运算符，用于计算矩阵与向量的乘积。从而将其转换到世界坐标系中
    normal = obj.matrix_world.to_3x3() @ face.normal
    bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    min_z = min(v.z for v in bbox)
    max_z = max(v.z for v in bbox)

    # 面中心位置
    face_center = sum((obj.matrix_world @ obj.data.vertices[vertex].co for vertex in face.vertices), mathutils.Vector()) / len(face.vertices)

    # 排除内表面：面法线应指向外部
    if normal.z > 0 and face_center.z > min_z + (max_z - min_z) * 0.1:
        return True
    if normal.z < 0 and face_center.z < max_z - (max_z - min_z) * 0.1:
        return True

    return False

def is_convex_face(face, obj):
    # 检查面是否是凹陷处
    # 简化实现：如果面法线的z值为负，说明面可能是凹陷处
    normal = obj.matrix_world.to_3x3() @ face.normal
    return normal.z > 0

def get_random_exterior_point_on_surface(obj, num_samples=10, top_ratio=0.1, bottom_ratio=0.1, min_distance_from_bottom=0.2):
    # 获取物体的网格数据
    mesh = obj.data
    faces = mesh.polygons

    # 获取物体的边界框
    bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    min_z = min(v.z for v in bbox)
    max_z = max(v.z for v in bbox)

    # 排除顶部和底部区域
    top_limit = max_z - (max_z - min_z) * top_ratio
    bottom_limit = min_z + (max_z - min_z) * bottom_ratio

    # 随机选择一个外表面
    for _ in range(num_samples):
        face = random.choice(faces)
        if not is_exterior_face(face, obj) or not is_convex_face(face, obj):
            continue
        
        # 计算面中心
        face_center = sum((obj.matrix_world @ obj.data.vertices[vertex].co for vertex in face.vertices), mathutils.Vector()) / len(face.vertices)
        # 获取面法线
        normal = obj.matrix_world.to_3x3() @ face.normal
        
        # 排除顶部和底部区域
        if face_center.z > top_limit or face_center.z < bottom_limit:
            continue
        
        # 确保与底面有一定距离
        if face_center.z < min_z + min_distance_from_bottom:
            continue
        
        return face_center, normal
    
    return None, None

def place_object_on_surface(source_object, target_object):
    location, normal = get_random_exterior_point_on_surface(target_object)
    if location is None:
        print("未能找到符合要求的表面位置。")
        return
    
    # 复制源物体
    new_object = source_object.copy()
    new_object.data = source_object.data.copy()
    bpy.context.collection.objects.link(new_object)
    
    # 设置新物体的位置
    new_object.location = location
    
    # 计算旋转
    z_axis = normal.normalized()
    x_axis = mathutils.Vector((1, 0, 0))
    y_axis = z_axis.cross(x_axis).normalized()
    x_axis = y_axis.cross(z_axis).normalized()
    
    rotation_matrix = mathutils.Matrix([x_axis, y_axis, z_axis]).transposed()
    new_object.rotation_euler = rotation_matrix.to_euler()
    
    # 随机缩放
    scale_x = random.uniform(0.5, 1.0)
    scale_y = random.uniform(0.5, 1.0)
    scale_z = random.uniform(0.5, 1.0)
    new_object.scale = (scale_x, scale_y, scale_z)
    
    return new_object

# 查找名为 'Tiny' 和 'Mushroom' 的物体
source_object = bpy.data.objects.get("Tiny")
target_object = bpy.data.objects.get("Mushroom")

if source_object is None or target_object is None:
    print("没有找到 'Tiny' 或 'Mushroom' 物体。")
else:
    # 删除现有的Tiny物体（以 "Tiny_" 开头的物体），避免重复
    for obj in bpy.data.objects:
        if obj.name.startswith("Tiny_"):
            bpy.data.objects.remove(obj, do_unlink=True)

    for i in range(5):
        place_object_on_surface(source_object, target_object)
    
    print("5个Tiny物体已创建并吸附在Mushroom的外侧表面（排除了内部、凹陷处、顶部、底部区域，并距离底面有一定距离）。")
