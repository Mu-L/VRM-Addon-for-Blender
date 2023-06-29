#!/usr/bin/env python3

import glob
import sys
from typing import List

from io_scene_vrm.common import deep, gltf
from io_scene_vrm.common.deep import Json


def clean(path: str) -> None:
    with open(path, "rb") as f:
        input_bin = f.read()

    json_dict, binary_chunk = gltf.parse_glb(input_bin)

    extensions_used = json_dict.get("extensionsUsed")
    if not isinstance(extensions_used, list):
        extensions_used = []
        json_dict["extensionsUsed"] = extensions_used
    extensions_used.clear()

    base_extensions_dicts: List[Json] = []
    base_extensions_dicts.append(json_dict)

    for mesh_dict in deep.get_list(json_dict, ["meshes"], []):
        base_extensions_dicts.append(mesh_dict)

    for material_dict in deep.get_list(json_dict, ["materials"], []):
        if not isinstance(material_dict, dict):
            continue
        base_extensions_dicts.append(material_dict)
        base_extensions_dicts.append(
            deep.get(material_dict, ["pbrMetallicRoughness", "baseColorTexture"])
        )
        base_extensions_dicts.append(
            deep.get(
                material_dict, ["pbrMetallicRoughness", "metallicRoughnessTexture"]
            )
        )
        base_extensions_dicts.append(material_dict.get("normalTexture"))
        base_extensions_dicts.append(material_dict.get("emissiveTexture"))
        base_extensions_dicts.append(material_dict.get("occlusionTexture"))

    for base_extensions_dict in base_extensions_dicts:
        if not isinstance(base_extensions_dict, dict):
            continue
        extensions_dict = base_extensions_dict.get("extensions")
        if not isinstance(extensions_dict, dict):
            continue
        for key in extensions_dict:
            if key not in extensions_used:
                extensions_used.append(key)

    extensions_used.sort()

    output_bin = gltf.pack_glb(json_dict, binary_chunk)

    with open(path, "wb") as f:
        f.write(output_bin)


def main() -> int:
    for path in glob.glob("**/*.vrm", recursive=True):
        print(f"===== {path} =====")
        clean(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())