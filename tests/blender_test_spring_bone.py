import math
import sys
from typing import List, Sequence

import bpy
from mathutils import Euler, Quaternion

from io_scene_vrm.common import version
from io_scene_vrm.editor.extension import VrmAddonArmatureExtensionPropertyGroup

addon_version = version.addon_version()
spec_version = VrmAddonArmatureExtensionPropertyGroup.SPEC_VERSION_VRM1


def get_test_command_args() -> List[List[str]]:
    return [[key.__name__] for key in FUNCTIONS]


def assert_vector3_equals(
    expected: Sequence[float], actual: Sequence[float], message: str
) -> None:
    if len(expected) != 3:
        raise AssertionError(f"expected length is not 3: {expected}")
    if len(actual) != 3:
        raise AssertionError(f"actual length is not 3: {actual}")

    threshold = 0.0001
    if abs(expected[0] - actual[0]) > threshold:
        raise AssertionError(
            f"{message}: {tuple(expected)} is different from {tuple(actual)}"
        )
    if abs(expected[1] - actual[1]) > threshold:
        raise AssertionError(
            f"{message}: {tuple(expected)} is different from {tuple(actual)}"
        )
    if abs(expected[2] - actual[2]) > threshold:
        raise AssertionError(
            f"{message}: {tuple(expected)} is different from {tuple(actual)}"
        )


def clean_scene() -> None:
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    while bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections[0])
    if bpy.app.version < (2, 93):
        bpy.ops.outliner.orphans_purge()
    else:
        bpy.ops.outliner.orphans_purge(do_recursive=True)


def one_joint_extending_in_y_direction() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 1, 0)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 2, 0)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 3, 0)
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].drag_force = 1
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].drag_force = 1
    joints[1].stiffness = 0

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "初期状態のjoint1")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1.7071, -0.7071), "1秒後のjoint1"
    )

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=10000)
    bpy.context.view_layer.update()

    assert_vector3_equals(
        armature.pose.bones["joint0"].head, (0, 1, 0), "10000秒後のjoint0"
    )
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1, -1), "10000秒後のjoint1"
    )


def one_joint_extending_in_y_direction_with_rotating_armature() -> None:
    clean_scene()

    bpy.ops.object.add(
        type="ARMATURE", location=(1, 0, 0), rotation=(0, 0, math.pi / 2)
    )
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0.1, 0)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 1.1, 0)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 2.1, 0)
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].drag_force = 1
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].drag_force = 1
    joints[1].stiffness = 0

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "初期状態のjoint1")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1.7071, -0.7071), "1秒後のjoint1"
    )

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=100000)
    bpy.context.view_layer.update()

    assert_vector3_equals(
        armature.pose.bones["joint0"].head, (0, 1, 0), "100000秒後のjoint0"
    )
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1, -1), "100000秒後のjoint1"
    )


def two_joints_extending_in_y_direction() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0.1, 0)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 1.1, 0)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 2.1, 0)

    joint_bone2 = armature.data.edit_bones.new("joint2")
    joint_bone2.parent = joint_bone1
    joint_bone2.head = (0, 3, 0)
    joint_bone2.tail = (0, 3.1, 0)
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].drag_force = 1
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].drag_force = 1
    joints[1].stiffness = 0
    joints[2].node.value = "joint2"
    joints[2].gravity_power = 1
    joints[2].drag_force = 1
    joints[2].stiffness = 0

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "初期状態のjoint1")
    assert_vector3_equals(armature.pose.bones["joint2"].head, (0, 3, 0), "初期状態のjoint2")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1.7071, -0.7071), "1秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 2.6824, -0.9280), "1秒後のjoint2"
    )

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=100000)
    bpy.context.view_layer.update()

    assert_vector3_equals(
        armature.pose.bones["joint0"].head, (0, 1, 0), "100000秒後のjoint0"
    )
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1, -1), "100000秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 1, -2), "100000秒後のjoint2"
    )


def two_joints_extending_in_y_direction_roll() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0.1, 0)
    root_bone.roll = math.radians(90)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 1.1, 0)
    joint_bone0.roll = math.radians(45)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 2.1, 0)
    joint_bone1.roll = math.radians(45)

    joint_bone2 = armature.data.edit_bones.new("joint2")
    joint_bone2.parent = joint_bone1
    joint_bone2.head = (0, 3, 0)
    joint_bone2.tail = (0, 3.1, 0)
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].drag_force = 1
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].drag_force = 1
    joints[1].stiffness = 0
    joints[2].node.value = "joint2"
    joints[2].gravity_power = 1
    joints[2].drag_force = 1
    joints[2].stiffness = 0

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "初期状態のjoint1")
    assert_vector3_equals(armature.pose.bones["joint2"].head, (0, 3, 0), "初期状態のjoint2")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1.7071, -0.7071), "1秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 2.6824, -0.9280), "1秒後のjoint2"
    )

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=100000)
    bpy.context.view_layer.update()

    assert_vector3_equals(
        armature.pose.bones["joint0"].head, (0, 1, 0), "100000秒後のjoint0"
    )
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1, -1), "100000秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 1, -2), "100000秒後のjoint2"
    )


def two_joints_extending_in_y_direction_local_translation() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0.1, 0)
    root_bone.use_local_location = True

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 1.1, 0)
    joint_bone0.use_local_location = True

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 2.1, 0)
    joint_bone1.use_local_location = True

    joint_bone2 = armature.data.edit_bones.new("joint2")
    joint_bone2.parent = joint_bone1
    joint_bone2.head = (0, 3, 0)
    joint_bone2.tail = (0, 3.1, 0)
    joint_bone2.use_local_location = False
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].drag_force = 1
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].drag_force = 1
    joints[1].stiffness = 0
    joints[2].node.value = "joint2"
    joints[2].gravity_power = 1
    joints[2].drag_force = 1
    joints[2].stiffness = 0

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "初期状態のjoint1")
    assert_vector3_equals(armature.pose.bones["joint2"].head, (0, 3, 0), "初期状態のjoint2")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1.7071, -0.7071), "1秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 2.6824, -0.9280), "1秒後のjoint2"
    )

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=100000)
    bpy.context.view_layer.update()

    assert_vector3_equals(
        armature.pose.bones["joint0"].head, (0, 1, 0), "100000秒後のjoint0"
    )
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1, -1), "100000秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 1, -2), "100000秒後のjoint2"
    )


def two_joints_extending_in_y_direction_connected() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 1, 0)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 2, 0)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 3, 0)

    joint_bone2 = armature.data.edit_bones.new("joint2")
    joint_bone2.parent = joint_bone1
    joint_bone2.head = (0, 3, 0)
    joint_bone2.tail = (0, 4, 0)

    joint_bone0.use_connect = True
    joint_bone1.use_connect = True
    joint_bone2.use_connect = True
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].drag_force = 1
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].drag_force = 1
    joints[1].stiffness = 0
    joints[2].node.value = "joint2"
    joints[2].gravity_power = 1
    joints[2].drag_force = 1
    joints[2].stiffness = 0

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "初期状態のjoint1")
    assert_vector3_equals(armature.pose.bones["joint2"].head, (0, 3, 0), "初期状態のjoint2")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1.7071, -0.7071), "1秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 2.6824, -0.9280), "1秒後のjoint2"
    )

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=100000)
    bpy.context.view_layer.update()

    assert_vector3_equals(
        armature.pose.bones["joint0"].head, (0, 1, 0), "100000秒後のjoint0"
    )
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1, -1), "100000秒後のjoint1"
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head, (0, 1, -2), "100000秒後のjoint2"
    )


def one_joint_extending_in_y_direction_gravity_y_object_move_to_z() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 1, 0)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 2, 0)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 3, 0)
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].gravity_dir = (0, 1, 0)
    joints[0].drag_force = 0
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].gravity_dir = (0, 1, 0)
    joints[1].drag_force = 0
    joints[1].stiffness = 0

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "初期状態のjoint1")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 2, 0), "1秒後のjoint1")

    armature.location = (0, 0, 1)
    bpy.context.view_layer.update()
    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "2秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head,
        (0, 1.8944271802, -0.4472135901),
        "2秒後のjoint1",
    )

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1000000)
    bpy.context.view_layer.update()

    assert_vector3_equals(
        armature.pose.bones["joint0"].head, (0, 1, 0), "1000000秒後のjoint0"
    )
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 2, 0), "1000000秒後のjoint1"
    )


def one_joint_extending_in_y_direction_rounding_180_degree() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 1, 0)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 2, 0)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 3, 0)
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1  # はじめに重力で勢いをつける
    joints[0].drag_force = 0
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 0
    joints[1].drag_force = 0
    joints[1].stiffness = 0

    armature.pose.bones["joint0"].rotation_mode = "QUATERNION"
    armature.pose.bones["joint0"].rotation_quaternion.rotate(Euler((0, math.pi, 0)))

    bpy.context.view_layer.update()

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 1, 0), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head, (0, 1.7071, -0.7071), "1秒後のjoint1"
    )


def two_joints_extending_in_y_direction_root_down() -> None:
    clean_scene()

    bpy.ops.object.add(type="ARMATURE", location=(0, 0, 0))
    armature = bpy.context.object
    armature.data.vrm_addon_extension.addon_version = addon_version
    armature.data.vrm_addon_extension.spec_version = spec_version
    armature.data.vrm_addon_extension.spring_bone1.enable_animation = True

    bpy.ops.object.mode_set(mode="EDIT")
    root_bone = armature.data.edit_bones.new("root")
    root_bone.head = (0, 0, 0)
    root_bone.tail = (0, 0.8, 0)

    joint_bone0 = armature.data.edit_bones.new("joint0")
    joint_bone0.parent = root_bone
    joint_bone0.head = (0, 1, 0)
    joint_bone0.tail = (0, 1.8, 0)

    joint_bone1 = armature.data.edit_bones.new("joint1")
    joint_bone1.parent = joint_bone0
    joint_bone1.head = (0, 2, 0)
    joint_bone1.tail = (0, 2.8, 0)

    joint_bone2 = armature.data.edit_bones.new("joint2")
    joint_bone2.parent = joint_bone1
    joint_bone2.head = (0, 3, 0)
    joint_bone2.tail = (0, 3.8, 0)
    bpy.ops.object.mode_set(mode="OBJECT")

    assert bpy.ops.vrm.add_spring_bone1_spring(armature_name=armature.name) == {
        "FINISHED"
    }
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}
    assert bpy.ops.vrm.add_spring_bone1_spring_joint(
        armature_name=armature.name, spring_index=0
    ) == {"FINISHED"}

    joints = armature.data.vrm_addon_extension.spring_bone1.springs[0].joints
    joints[0].node.value = "joint0"
    joints[0].gravity_power = 1
    joints[0].drag_force = 1
    joints[0].stiffness = 0
    joints[1].node.value = "joint1"
    joints[1].gravity_power = 1
    joints[1].drag_force = 1
    joints[1].stiffness = 0
    joints[2].node.value = "joint2"
    joints[2].gravity_power = 1
    joints[2].drag_force = 1
    joints[2].stiffness = 0

    root_pose_bone = armature.pose.bones["root"]
    if root_pose_bone.rotation_mode != "QUATERNION":
        root_pose_bone.rotation_mode = "QUATERNION"
    root_pose_bone.rotation_quaternion = Quaternion((1, 0, 0), math.radians(-90.0))

    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 0, -1), "初期状態のjoint0")
    assert_vector3_equals(armature.pose.bones["joint1"].head, (0, 0, -2), "初期状態のjoint1")
    assert_vector3_equals(armature.pose.bones["joint2"].head, (0, 0, -3), "初期状態のjoint2")

    bpy.ops.vrm.update_spring_bone1_animation(delta_time=1)
    bpy.context.view_layer.update()

    assert_vector3_equals(armature.pose.bones["joint0"].head, (0, 0, -1), "1秒後のjoint0")
    assert_vector3_equals(
        armature.pose.bones["joint1"].head,
        (0, 0, -2),
        "1秒後のjoint1",
    )
    assert_vector3_equals(
        armature.pose.bones["joint2"].head,
        (0, 0, -3),
        "1秒後のjoint2",
    )


FUNCTIONS = [
    one_joint_extending_in_y_direction,
    one_joint_extending_in_y_direction_gravity_y_object_move_to_z,
    one_joint_extending_in_y_direction_with_rotating_armature,
    one_joint_extending_in_y_direction_rounding_180_degree,
    two_joints_extending_in_y_direction,
    two_joints_extending_in_y_direction_root_down,
    two_joints_extending_in_y_direction_roll,
    two_joints_extending_in_y_direction_connected,
    two_joints_extending_in_y_direction_local_translation,
]


def test(function_name: str) -> None:
    function = {0: f for f in FUNCTIONS if f.__name__ == function_name}.get(0)
    if function is None:
        raise AssertionError(f"No function name: {function_name}")
    function()


if __name__ == "__main__":
    if "--" in sys.argv:
        test(*sys.argv[slice(sys.argv.index("--") + 1, sys.maxsize)])
    else:
        for arg in get_test_command_args():
            test(*arg)
