import functools
import sys
from collections.abc import Sequence
from sys import float_info
from typing import Optional

import bpy
from bpy.app.translations import pgettext

from ...common.logging import get_logger
from ...common.vrm1.human_bone import (
    HumanBoneName,
    HumanBoneSpecification,
    HumanBoneSpecifications,
)
from ..property_group import (
    BonePropertyGroup,
    MeshObjectPropertyGroup,
    StringPropertyGroup,
)

logger = get_logger(__name__)


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.humanoid.humanBones.humanBone.schema.json
class Vrm1HumanBonePropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    node: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=BonePropertyGroup  # noqa: F722
    )

    # for UI
    node_candidates: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=StringPropertyGroup
    )

    def update_node_candidates(
        self,
        armature_data: bpy.types.Armature,
        target: HumanBoneSpecification,
        bpy_bone_name_to_human_bone_specification: dict[str, HumanBoneSpecification],
    ) -> None:
        new_candidates = BonePropertyGroup.find_bone_candidates(
            armature_data,
            target,
            bpy_bone_name_to_human_bone_specification,
        )
        if set(n.value for n in self.node_candidates) == new_candidates:
            return

        self.node_candidates.clear()
        # Preserving list order
        for bone_name in armature_data.bones.keys():
            if bone_name not in new_candidates:
                continue
            candidate = self.node_candidates.add()
            candidate.value = bone_name


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.humanoid.humanBones.schema.json
class Vrm1HumanBonesPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    hips: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    spine: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    chest: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    upper_chest: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    neck: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    head: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_eye: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_eye: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    jaw: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_upper_leg: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_lower_leg: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_foot: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_toes: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_upper_leg: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_lower_leg: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_foot: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_toes: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_shoulder: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_upper_arm: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_lower_arm: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_hand: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_shoulder: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_upper_arm: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_lower_arm: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_hand: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_thumb_metacarpal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_thumb_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_thumb_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_index_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_index_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_index_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_middle_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_middle_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_middle_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_ring_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_ring_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_ring_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_little_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_little_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    left_little_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_thumb_metacarpal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_thumb_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_thumb_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_index_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_index_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_index_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_middle_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_middle_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_middle_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_ring_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_ring_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_ring_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_little_proximal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_little_intermediate: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )
    right_little_distal: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanBonePropertyGroup  # noqa: F722
    )

    # for UI
    last_bone_names: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=StringPropertyGroup
    )
    initial_automatic_bone_assignment: bpy.props.BoolProperty(  # type: ignore[valid-type]
        default=True
    )

    def human_bone_name_to_human_bone(
        self,
    ) -> dict[HumanBoneName, Vrm1HumanBonePropertyGroup]:
        return {
            HumanBoneName.HIPS: self.hips,
            HumanBoneName.SPINE: self.spine,
            HumanBoneName.CHEST: self.chest,
            HumanBoneName.UPPER_CHEST: self.upper_chest,
            HumanBoneName.NECK: self.neck,
            HumanBoneName.HEAD: self.head,
            HumanBoneName.LEFT_EYE: self.left_eye,
            HumanBoneName.RIGHT_EYE: self.right_eye,
            HumanBoneName.JAW: self.jaw,
            HumanBoneName.LEFT_UPPER_LEG: self.left_upper_leg,
            HumanBoneName.LEFT_LOWER_LEG: self.left_lower_leg,
            HumanBoneName.LEFT_FOOT: self.left_foot,
            HumanBoneName.LEFT_TOES: self.left_toes,
            HumanBoneName.RIGHT_UPPER_LEG: self.right_upper_leg,
            HumanBoneName.RIGHT_LOWER_LEG: self.right_lower_leg,
            HumanBoneName.RIGHT_FOOT: self.right_foot,
            HumanBoneName.RIGHT_TOES: self.right_toes,
            HumanBoneName.LEFT_SHOULDER: self.left_shoulder,
            HumanBoneName.LEFT_UPPER_ARM: self.left_upper_arm,
            HumanBoneName.LEFT_LOWER_ARM: self.left_lower_arm,
            HumanBoneName.LEFT_HAND: self.left_hand,
            HumanBoneName.RIGHT_SHOULDER: self.right_shoulder,
            HumanBoneName.RIGHT_UPPER_ARM: self.right_upper_arm,
            HumanBoneName.RIGHT_LOWER_ARM: self.right_lower_arm,
            HumanBoneName.RIGHT_HAND: self.right_hand,
            HumanBoneName.LEFT_THUMB_METACARPAL: self.left_thumb_metacarpal,
            HumanBoneName.LEFT_THUMB_PROXIMAL: self.left_thumb_proximal,
            HumanBoneName.LEFT_THUMB_DISTAL: self.left_thumb_distal,
            HumanBoneName.LEFT_INDEX_PROXIMAL: self.left_index_proximal,
            HumanBoneName.LEFT_INDEX_INTERMEDIATE: self.left_index_intermediate,
            HumanBoneName.LEFT_INDEX_DISTAL: self.left_index_distal,
            HumanBoneName.LEFT_MIDDLE_PROXIMAL: self.left_middle_proximal,
            HumanBoneName.LEFT_MIDDLE_INTERMEDIATE: self.left_middle_intermediate,
            HumanBoneName.LEFT_MIDDLE_DISTAL: self.left_middle_distal,
            HumanBoneName.LEFT_RING_PROXIMAL: self.left_ring_proximal,
            HumanBoneName.LEFT_RING_INTERMEDIATE: self.left_ring_intermediate,
            HumanBoneName.LEFT_RING_DISTAL: self.left_ring_distal,
            HumanBoneName.LEFT_LITTLE_PROXIMAL: self.left_little_proximal,
            HumanBoneName.LEFT_LITTLE_INTERMEDIATE: self.left_little_intermediate,
            HumanBoneName.LEFT_LITTLE_DISTAL: self.left_little_distal,
            HumanBoneName.RIGHT_THUMB_METACARPAL: self.right_thumb_metacarpal,
            HumanBoneName.RIGHT_THUMB_PROXIMAL: self.right_thumb_proximal,
            HumanBoneName.RIGHT_THUMB_DISTAL: self.right_thumb_distal,
            HumanBoneName.RIGHT_INDEX_PROXIMAL: self.right_index_proximal,
            HumanBoneName.RIGHT_INDEX_INTERMEDIATE: self.right_index_intermediate,
            HumanBoneName.RIGHT_INDEX_DISTAL: self.right_index_distal,
            HumanBoneName.RIGHT_MIDDLE_PROXIMAL: self.right_middle_proximal,
            HumanBoneName.RIGHT_MIDDLE_INTERMEDIATE: self.right_middle_intermediate,
            HumanBoneName.RIGHT_MIDDLE_DISTAL: self.right_middle_distal,
            HumanBoneName.RIGHT_RING_PROXIMAL: self.right_ring_proximal,
            HumanBoneName.RIGHT_RING_INTERMEDIATE: self.right_ring_intermediate,
            HumanBoneName.RIGHT_RING_DISTAL: self.right_ring_distal,
            HumanBoneName.RIGHT_LITTLE_PROXIMAL: self.right_little_proximal,
            HumanBoneName.RIGHT_LITTLE_INTERMEDIATE: self.right_little_intermediate,
            HumanBoneName.RIGHT_LITTLE_DISTAL: self.right_little_distal,
        }

    def error_messages(self) -> list[str]:
        messages = []

        human_bone_name_to_human_bone = self.human_bone_name_to_human_bone()
        for name, human_bone in human_bone_name_to_human_bone.items():
            specification = HumanBoneSpecifications.get(name)
            if not human_bone.node.bone_name:
                if specification.requirement:
                    messages.append(
                        pgettext('Please assign Required VRM Bone "{name}".').format(
                            name=specification.title
                        )
                    )
                continue
            if not specification.parent_requirement:
                continue
            if not specification.parent_name:
                logger.error(f"No parent for '{name}' in spec")
                continue
            parent = human_bone_name_to_human_bone.get(specification.parent_name)
            if not parent:
                logger.error(f"No parent for '{name}' in dict")
                continue
            parent_specification = specification.parent()
            if not parent_specification:
                logger.error(f"No parent specification for '{name}'")
                continue
            if not parent.node.bone_name:
                messages.append(
                    pgettext(
                        'Please assign "{parent_name}" because "{name}" requires it as its child bone.'
                    ).format(
                        name=specification.title, parent_name=parent_specification.title
                    )
                )

        return messages

    def all_required_bones_are_assigned(self) -> bool:
        return len(self.error_messages()) == 0

    @staticmethod
    def fixup_human_bones(obj: bpy.types.Object) -> None:
        armature_data = obj.data
        if (
            obj.type != "ARMATURE"
            or not isinstance(armature_data, bpy.types.Armature)
            or not hasattr(armature_data, "vrm_addon_extension")
        ):
            return

        human_bones = armature_data.vrm_addon_extension.vrm1.humanoid.human_bones

        # 複数のボーンマップに同一のBlenderのボーンが設定されていたら片方を削除
        fixup = True
        while fixup:
            fixup = False
            found_node_bone_names = []
            for human_bone in human_bones.human_bone_name_to_human_bone().values():
                if not human_bone.node.bone_name:
                    continue
                if human_bone.node.bone_name not in found_node_bone_names:
                    found_node_bone_names.append(human_bone.node.bone_name)
                    continue
                human_bone.node.bone_name = ""
                fixup = True
                break

    @staticmethod
    def check_last_bone_names_and_update(
        armature_data_name: str,
        defer: bool = True,
    ) -> None:
        armature_data = bpy.data.armatures.get(armature_data_name)
        if not isinstance(armature_data, bpy.types.Armature):
            return
        human_bones = armature_data.vrm_addon_extension.vrm1.humanoid.human_bones
        bone_names = []
        for bone in sorted(armature_data.bones.values(), key=lambda b: str(b.name)):
            bone_names.append(bone.name)
            bone_names.append(bone.parent.name if bone.parent else "")
        up_to_date = bone_names == [str(n.value) for n in human_bones.last_bone_names]

        if up_to_date:
            return

        if defer:
            bpy.app.timers.register(
                functools.partial(
                    Vrm1HumanBonesPropertyGroup.check_last_bone_names_and_update,
                    armature_data_name,
                    False,
                )
            )
            return

        human_bones.last_bone_names.clear()
        for bone_name in bone_names:
            last_bone_name = human_bones.last_bone_names.add()
            last_bone_name.value = bone_name
        bpy_bone_name_to_human_bone_specification: dict[str, HumanBoneSpecification] = {
            human_bone.node.bone_name: HumanBoneSpecifications.get(human_bone_name)
            for human_bone_name, human_bone in human_bones.human_bone_name_to_human_bone().items()
            if human_bone.node.bone_name
        }

        for (
            human_bone_name,
            human_bone,
        ) in human_bones.human_bone_name_to_human_bone().items():
            human_bone.update_node_candidates(
                armature_data,
                HumanBoneSpecifications.get(human_bone_name),
                bpy_bone_name_to_human_bone_specification,
            )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.humanoid.schema.json
class Vrm1HumanoidPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    human_bones: bpy.props.PointerProperty(type=Vrm1HumanBonesPropertyGroup)  # type: ignore[valid-type]

    # for T-Pose
    def update_pose_library(self, _context: bpy.types.Context) -> None:
        self.pose_marker_name = ""

    pose_library: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=bpy.types.Action,
        update=update_pose_library,
    )
    pose_marker_name: bpy.props.StringProperty()  # type: ignore[valid-type]


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.lookAt.rangeMap.schema.json
class Vrm1LookAtRangeMapPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    input_max_value: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Input Max Value",  # noqa: F722
        min=0.0001,  # https://github.com/pixiv/three-vrm/issues/1197#issuecomment-1498492002
        default=90.0,
        max=180.0,
    )
    output_scale: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Output Scale",  # noqa: F722
        default=10.0,
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.lookAt.schema.json
class Vrm1LookAtPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    offset_from_head_bone: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Offset From Head Bone",  # noqa: F722
        size=3,
        subtype="TRANSLATION",  # noqa: F821
        unit="LENGTH",  # noqa: F821
        default=(0, 0, 0),
    )
    type_items = [
        ("bone", "Bone", "Bone", "BONE_DATA", 0),
        ("expression", "Expression", "Expression", "SHAPEKEY_DATA", 1),
    ]
    type: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Type",  # noqa: F821
        items=type_items,
    )
    range_map_horizontal_inner: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1LookAtRangeMapPropertyGroup,
    )
    range_map_horizontal_outer: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1LookAtRangeMapPropertyGroup,
    )
    range_map_vertical_down: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1LookAtRangeMapPropertyGroup,
    )
    range_map_vertical_up: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1LookAtRangeMapPropertyGroup,
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.firstPerson.meshAnnotation.schema.json
class Vrm1MeshAnnotationPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    node: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=MeshObjectPropertyGroup  # noqa: F821
    )
    type_items = [
        ("auto", "Auto", "", 0),
        ("both", "Both", "", 1),
        ("thirdPersonOnly", "Third-Person Only", "", 2),
        ("firstPersonOnly", "First-Person Only", "", 3),
    ]
    type: bpy.props.EnumProperty(  # type: ignore[valid-type]
        items=type_items, name="First Person Type"  # noqa: F722
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.firstPerson.schema.json
class Vrm1FirstPersonPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    mesh_annotations: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        name="Mesh Annotations", type=Vrm1MeshAnnotationPropertyGroup  # noqa: F722
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.expressions.expression.morphTargetBind.schema.json
class Vrm1MorphTargetBindPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    node: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=MeshObjectPropertyGroup  # noqa: F821
    )
    index: bpy.props.StringProperty(  # type: ignore[valid-type]
        # noqa: F821
    )
    weight: bpy.props.FloatProperty(  # type: ignore[valid-type]
        min=0, default=1, max=1  # noqa: F821
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.expressions.expression.materialColorBind.schema.json
class Vrm1MaterialColorBindPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    material: bpy.props.PointerProperty(  # type: ignore[valid-type]
        name="Material",  # noqa: F821
        type=bpy.types.Material,  # noqa: F821
    )

    type_items = [
        ("color", "Color", "", 0),
        ("emissionColor", "Emission Color", "", 1),
        ("shadeColor", "Shade Color", "", 2),
        ("matcapColor", "Matcap Color", "", 5),
        ("rimColor", "Rim Color", "", 3),
        ("outlineColor", "Outline Color", "", 4),
    ]
    type: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Type",  # noqa: F821
        items=type_items,  # noqa: F722
    )
    target_value: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Target Value",  # noqa: F722
        size=4,  # noqa: F722
        subtype="COLOR",  # noqa: F821
        min=0,
        max=1,  # TODO: hdr emission color?
    )

    def get_target_value_as_rgb(self) -> tuple[float, float, float]:
        return (
            float(self.target_value[0]),
            float(self.target_value[1]),
            float(self.target_value[2]),
        )

    def set_target_value_as_rgb(self, value: Sequence[float]) -> None:
        if len(value) < 3:
            return
        self.target_value = (
            float(value[0]),
            float(value[1]),
            float(value[2]),
            float(self.target_value[3]),
        )

    target_value_as_rgb: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        name="Target Value",  # noqa: F722
        size=3,  # noqa: F722
        subtype="COLOR",  # noqa: F821
        get=get_target_value_as_rgb,
        set=set_target_value_as_rgb,
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.expressions.expression.textureTransformBind.schema.json
class Vrm1TextureTransformBindPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    material: bpy.props.PointerProperty(  # type: ignore[valid-type]
        name="Material",  # noqa: F821
        type=bpy.types.Material,  # noqa: F821
    )
    scale: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        size=2, default=(1, 1)  # noqa: F722
    )
    offset: bpy.props.FloatVectorProperty(  # type: ignore[valid-type]
        size=2, default=(0, 0)  # noqa: F722
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.expressions.expression.schema.json
class Vrm1ExpressionPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    morph_target_binds: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=Vrm1MorphTargetBindPropertyGroup  # noqa: F821
    )
    material_color_binds: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=Vrm1MaterialColorBindPropertyGroup  # noqa: F722
    )
    texture_transform_binds: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=Vrm1TextureTransformBindPropertyGroup  # noqa: F722
    )
    is_binary: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Is Binary"  # noqa: F722
    )

    expression_override_type_items = [
        ("none", "None", "", 0),
        ("block", "Block", "", 1),
        ("blend", "Blend", "", 2),
    ]
    EXPRESSION_OVERRIDE_TYPE_VALUES = [
        expression_override_type_item[0]
        for expression_override_type_item in expression_override_type_items
    ]

    override_blink: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Override Blink", items=expression_override_type_items  # noqa: F722
    )
    override_look_at: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Override Look At", items=expression_override_type_items  # noqa: F722
    )
    override_mouth: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Override Mouth", items=expression_override_type_items  # noqa: F722
    )

    # for UI
    show_expanded: bpy.props.BoolProperty()  # type: ignore[valid-type]
    show_expanded_morph_target_binds: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Morph Target Binds"  # noqa: F722
    )
    show_expanded_material_color_binds: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Material Color Binds"  # noqa: F722
    )
    show_expanded_texture_transform_binds: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Texture Transform Binds"  # noqa: F722
    )

    # アニメーション再生中はframe_change_pre/frame_change_postでしかシェイプキーの値の変更ができないので、
    # 変更された値をここに保存しておく
    frame_change_post_shape_key_updates: dict[tuple[str, str], float] = {}

    def get_preview(self) -> float:
        value = self.get("preview")
        if isinstance(value, (float, int)):
            return float(value)
        return 0.0

    def set_preview(self, value: object) -> None:
        if not isinstance(value, (int, float)):
            return

        current_value = self.get("preview")
        if (
            isinstance(current_value, (int, float))
            and abs(current_value - value) < float_info.epsilon
        ):
            return

        self["preview"] = float(value)

        blend_data = bpy.data
        for morph_target_bind in self.morph_target_binds:
            mesh_object = blend_data.objects.get(
                morph_target_bind.node.mesh_object_name
            )
            if not mesh_object or mesh_object.type != "MESH":
                continue
            mesh = mesh_object.data
            if not isinstance(mesh, bpy.types.Mesh):
                continue
            mesh_shape_keys = mesh.shape_keys
            if not mesh_shape_keys:
                continue
            shape_key = blend_data.shape_keys.get(mesh_shape_keys.name)
            if not shape_key:
                continue
            key_blocks = shape_key.key_blocks
            if not key_blocks:
                continue
            if morph_target_bind.index not in key_blocks:
                continue
            if self.is_binary:
                preview = 1.0 if self.preview > 0.0 else 0.0
            else:
                preview = self.preview
            key_block_value = (
                morph_target_bind.weight * preview
            )  # Lerp 0.0 * (1 - a) + weight * a
            key_blocks[morph_target_bind.index].value = key_block_value
            Vrm1ExpressionPropertyGroup.frame_change_post_shape_key_updates[
                (shape_key.name, morph_target_bind.index)
            ] = key_block_value

    preview: bpy.props.FloatProperty(  # type: ignore[valid-type]
        name="Expression",  # noqa: F821
        min=0,
        max=1,
        subtype="FACTOR",  # noqa: F821
        get=get_preview,  # noqa: F821
        set=set_preview,  # noqa: F821
    )

    active_morph_target_bind_index: bpy.props.IntProperty()  # type: ignore[valid-type]
    active_material_color_bind_index: bpy.props.IntProperty()  # type: ignore[valid-type]
    active_texture_transform_bind_index: bpy.props.IntProperty()  # type: ignore[valid-type]


class Vrm1CustomExpressionPropertyGroup(Vrm1ExpressionPropertyGroup):
    def get_custom_name(self) -> str:
        return str(self.get("custom_name", ""))

    def set_custom_name(self, value: str) -> None:
        if not value or self.get("custom_name") == value:
            return

        vrm1: Optional[Vrm1PropertyGroup] = None
        for search_armature in bpy.data.armatures:
            ext = search_armature.vrm_addon_extension
            for custom_expression in ext.vrm1.expressions.custom:
                if custom_expression != self:
                    continue
                vrm1 = search_armature.vrm_addon_extension.vrm1
                break
        if vrm1 is None:
            logger.error(f"No armature extension for {self}")
            return

        expressions = vrm1.expressions
        all_expression_names = expressions.all_name_to_expression_dict().keys()
        custom_name = value
        for index in range(sys.maxsize):
            if index > 0:
                custom_name = f"{value}.{index:03}"
            if custom_name not in all_expression_names:
                break

        self["custom_name"] = custom_name
        self.name = custom_name  # pylint: disable=attribute-defined-outside-init

    custom_name: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Name",  # noqa: F821
        get=get_custom_name,
        set=set_custom_name,
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.expressions.schema.json
class Vrm1ExpressionsPresetPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    happy: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    angry: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    sad: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    relaxed: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    surprised: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    neutral: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    aa: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    ih: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    ou: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    ee: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    oh: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    blink: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    blink_left: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    blink_right: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    look_up: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    look_down: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    look_left: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]
    look_right: bpy.props.PointerProperty(type=Vrm1ExpressionPropertyGroup)  # type: ignore[valid-type]

    def name_to_expression_dict(self) -> dict[str, Vrm1ExpressionPropertyGroup]:
        return {
            "happy": self.happy,
            "angry": self.angry,
            "sad": self.sad,
            "relaxed": self.relaxed,
            "surprised": self.surprised,
            "neutral": self.neutral,
            "aa": self.aa,
            "ih": self.ih,
            "ou": self.ou,
            "ee": self.ee,
            "oh": self.oh,
            "blink": self.blink,
            "blinkLeft": self.blink_left,
            "blinkRight": self.blink_right,
            "lookUp": self.look_up,
            "lookDown": self.look_down,
            "lookLeft": self.look_left,
            "lookRight": self.look_right,
        }


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.expressions.schema.json
class Vrm1ExpressionsPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    preset: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1ExpressionsPresetPropertyGroup,  # noqa: F722
    )

    custom: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=Vrm1CustomExpressionPropertyGroup,  # noqa: F722
    )

    def all_name_to_expression_dict(self) -> dict[str, Vrm1ExpressionPropertyGroup]:
        if not isinstance(self.preset, Vrm1ExpressionsPresetPropertyGroup):
            # make static type checker happy
            raise AssertionError("preset is not a Vrm1ExpressionsPresetPropertyGroup")

        result = self.preset.name_to_expression_dict()
        for custom_expression in self.custom:
            if not isinstance(custom_expression, Vrm1CustomExpressionPropertyGroup):
                # make static type checker happy
                raise AssertionError(
                    "custom_expression is not a Vrm1CustomExpressionPropertyGroup"
                )
            result[custom_expression.custom_name] = custom_expression
        return result

    # expressionのUIList表示のため、expressionの数だけ空の要素を持つ
    expression_ui_list_elements: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=StringPropertyGroup  # noqa: F821
    )
    active_expression_ui_list_element_index: bpy.props.IntProperty()  # type: ignore[valid-type]


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.meta.schema.json
class Vrm1MetaPropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    avatar_permission_items = [
        ("onlyAuthor", "Only Author", "", 0),
        ("onlySeparatelyLicensedPerson", "Only Separately Licensed Person", "", 1),
        ("everyone", "Everyone", "", 2),
    ]
    AVATAR_PERMISSION_VALUES = [
        avatar_permission_item[0] for avatar_permission_item in avatar_permission_items
    ]

    commercial_usage_items = [
        ("personalNonProfit", "Personal Non-Profit", "", 0),
        ("personalProfit", "Personal Profit", "", 1),
        ("corporation", "Corporation", "", 2),
    ]
    COMMERCIAL_USAGE_VALUES = [
        commercial_usage_item[0] for commercial_usage_item in commercial_usage_items
    ]

    credit_notation_items = [
        ("required", "Required", "", 0),
        ("unnecessary", "Unnecessary", "", 1),
    ]
    CREDIT_NOTATION_VALUES = [
        credit_notation_item[0] for credit_notation_item in credit_notation_items
    ]

    modification_items = [
        ("prohibited", "Prohibited", "", 0),
        ("allowModification", "Allow Modification", "", 1),
        ("allowModificationRedistribution", "Allow Modification Redistribution", "", 2),
    ]
    MODIFICATION_VALUES = [
        modification_item[0] for modification_item in modification_items
    ]

    vrm_name: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Name"  # noqa: F821
    )
    version: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Version"  # noqa: F821
    )
    authors: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=StringPropertyGroup  # noqa: F821
    )
    copyright_information: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Copyright Information"  # noqa: F722
    )
    contact_information: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Contact Information"  # noqa: F722
    )
    references: bpy.props.CollectionProperty(  # type: ignore[valid-type]
        type=StringPropertyGroup  # noqa: F821
    )
    third_party_licenses: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Third Party Licenses"  # noqa: F722
    )
    thumbnail_image: bpy.props.PointerProperty(  # type: ignore[valid-type]
        name="Thumbnail Image", type=bpy.types.Image  # noqa: F722
    )
    # license_url: bpy.props.StringProperty(  # type: ignore[valid-type]
    #     name="License URL"  # noqa: F722
    # )
    avatar_permission: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Avatar Permission",  # noqa: F722
        items=avatar_permission_items,
    )
    allow_excessively_violent_usage: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Allow Excessively Violent Usage"  # noqa: F722
    )
    allow_excessively_sexual_usage: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Allow Excessively Sexual Usage"  # noqa: F722
    )
    commercial_usage: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Commercial Usage",  # noqa: F722
        items=commercial_usage_items,
    )
    allow_political_or_religious_usage: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Allow Political or Religious Usage"  # noqa: F722
    )
    allow_antisocial_or_hate_usage: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Allow Antisocial or Hate Usage"  # noqa: F722
    )
    credit_notation: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Credit Notation",  # noqa: F722
        items=credit_notation_items,
    )
    allow_redistribution: bpy.props.BoolProperty(  # type: ignore[valid-type]
        name="Allow Redistribution"  # noqa: F722
    )
    modification: bpy.props.EnumProperty(  # type: ignore[valid-type]
        name="Modification", items=modification_items  # noqa: F821
    )
    other_license_url: bpy.props.StringProperty(  # type: ignore[valid-type]
        name="Other License URL"  # noqa: F722
    )


# https://github.com/vrm-c/vrm-specification/blob/6fb6baaf9b9095a84fb82c8384db36e1afeb3558/specification/VRMC_vrm-1.0-beta/schema/VRMC_vrm.schema.json
class Vrm1PropertyGroup(bpy.types.PropertyGroup):  # type: ignore[misc]
    meta: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1MetaPropertyGroup  # noqa: F722
    )
    humanoid: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1HumanoidPropertyGroup  # noqa: F722
    )
    first_person: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1FirstPersonPropertyGroup  # noqa: F722
    )
    look_at: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1LookAtPropertyGroup  # noqa: F722
    )
    expressions: bpy.props.PointerProperty(  # type: ignore[valid-type]
        type=Vrm1ExpressionsPropertyGroup  # noqa: F722
    )
