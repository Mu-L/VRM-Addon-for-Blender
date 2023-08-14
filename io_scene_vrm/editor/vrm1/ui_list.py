import bpy

from ...common.logging import get_logger
from .property_group import (
    Vrm1ExpressionsPropertyGroup,
    Vrm1MaterialColorBindPropertyGroup,
    Vrm1MorphTargetBindPropertyGroup,
    Vrm1TextureTransformBindPropertyGroup,
)

logger = get_logger(__name__)


class VRM_UL_vrm1_expression(bpy.types.UIList):  # type: ignore[misc]
    bl_idname = "VRM_UL_vrm1_expression"

    def draw_item(
        self,
        _context: bpy.types.Context,
        layout: bpy.types.UILayout,
        data: object,
        _item: object,
        _icon: int,
        _active_data: object,
        _active_prop_name: str,
        index: int,
        _flt_flag: int,
    ) -> None:
        expressions = data
        if not isinstance(expressions, Vrm1ExpressionsPropertyGroup):
            return
        preset_expression_items = list(
            expressions.preset.name_to_expression_dict().items()
        )
        if index < len(preset_expression_items):
            name, expression = preset_expression_items[index]
            icon = {
                "happy": "HEART",
                "angry": "ORPHAN_DATA",
                "sad": "MOD_FLUIDSIM",
                "relaxed": "LIGHT_SUN",
                "surprised": "LIGHT_SUN",
                "neutral": "VIEW_ORTHO",
                "aa": "EVENT_A",
                "ih": "EVENT_I",
                "ou": "EVENT_U",
                "ee": "EVENT_E",
                "oh": "EVENT_O",
                "blink": "HIDE_ON",
                "blinkLeft": "HIDE_ON",
                "blinkRight": "HIDE_ON",
                "lookUp": "ANCHOR_TOP",
                "lookDown": "ANCHOR_BOTTOM",
                "lookLeft": "ANCHOR_RIGHT",
                "lookRight": "ANCHOR_LEFT",
            }.get(name)
            if not icon:
                logger.error(f"Unknown preset expression: {name}")
                icon = "SHAPEKEY_DATA"
        else:
            custom_expressions = expressions.custom
            custom_index = index - len(preset_expression_items)
            if custom_index >= len(custom_expressions):
                return
            expression = custom_expressions[custom_index]
            name = expression.custom_name
            icon = "SHAPEKEY_DATA"

        if self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", translate=False, icon=icon)
            return

        if self.layout_type not in {"DEFAULT", "COMPACT"}:
            return

        split = layout.split(align=True, factor=0.55)
        split.label(text=name, translate=False, icon=icon)
        split.prop(expression, "preview", text="Preview")


class VRM_UL_vrm1_morph_target_bind(bpy.types.UIList):  # type: ignore[misc]
    bl_idname = "VRM_UL_vrm1_morph_target_bind"

    def draw_item(
        self,
        context: bpy.types.Context,
        layout: bpy.types.UILayout,
        _data: object,
        item: object,
        icon: int,
        _active_data: object,
        _active_prop_name: str,
        _index: int,
        _flt_flag: int,
    ) -> None:
        blend_data = context.blend_data
        morph_target_bind = item
        if not isinstance(morph_target_bind, Vrm1MorphTargetBindPropertyGroup):
            return

        if self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon_value=icon)
            return

        if self.layout_type not in {"DEFAULT", "COMPACT"}:
            return

        name = morph_target_bind.node.mesh_object_name
        mesh_object = blend_data.objects.get(morph_target_bind.node.mesh_object_name)
        if (
            mesh_object
            and mesh_object.type == "MESH"
            and mesh_object.data
            and mesh_object.data.shape_keys
        ):
            keys = mesh_object.data.shape_keys.key_blocks.keys()
            if morph_target_bind.index in keys:
                name += " / " + morph_target_bind.index
        layout.label(text=name, translate=False, icon="MESH_DATA")


class VRM_UL_vrm1_material_color_bind(bpy.types.UIList):  # type: ignore[misc]
    bl_idname = "VRM_UL_vrm0_material_color_bind"

    def draw_item(
        self,
        _context: bpy.types.Context,
        layout: bpy.types.UILayout,
        _data: object,
        item: object,
        icon: int,
        _active_data: object,
        _active_prop_name: str,
        _index: int,
        _flt_flag: int,
    ) -> None:
        material_color_bind = item
        if not isinstance(material_color_bind, Vrm1MaterialColorBindPropertyGroup):
            return

        if self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", translate=False, icon_value=icon)
            return

        if self.layout_type not in {"DEFAULT", "COMPACT"}:
            return

        name = ""
        if material_color_bind.material:
            name = material_color_bind.material.name + " / " + material_color_bind.type
        layout.label(text=name, translate=False, icon="MATERIAL")


class VRM_UL_vrm1_texture_transform_bind(bpy.types.UIList):  # type: ignore[misc]
    bl_idname = "VRM_UL_vrm1_texture_transform_bind"

    def draw_item(
        self,
        _context: bpy.types.Context,
        layout: bpy.types.UILayout,
        _data: object,
        item: object,
        icon: int,
        _active_data: object,
        _active_prop_name: str,
        _index: int,
        _flt_flag: int,
    ) -> None:
        texture_transform_bind = item
        if not isinstance(
            texture_transform_bind, Vrm1TextureTransformBindPropertyGroup
        ):
            return

        if self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", translate=False, icon_value=icon)
            return

        if self.layout_type not in {"DEFAULT", "COMPACT"}:
            return

        name = ""
        if texture_transform_bind.material:
            name = texture_transform_bind.material.name
        layout.label(text=name, translate=False, icon="MATERIAL")