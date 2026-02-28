# SPDX-License-Identifier: Apache-2.0
# https://projects.blender.org/blender/blender-addons/src/tag/v2.93.0/io_scene_gltf2/io/com/gltf2_io.py

from collections.abc import Sequence

class Material: ...
class Image: ...

class Gltf:
    images: Sequence[object] | None
    def to_dict(self) -> dict[object, object]: ...
