"""This script contains helper methods to import Ni based properties."""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright © 2020, NIF File Format Library and Tools contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

import bpy
from pyffi.formats.nif import NifFormat

from io_scene_nif.modules.nif_import.animation.material import MaterialAnimation
from io_scene_nif.modules.nif_import.property.material import Material, NiMaterial
from io_scene_nif.modules.nif_import.property.texture.types.nitextureprop import NiTextureProp
from io_scene_nif.utils.util_global import NifData
from io_scene_nif.utils.util_logging import NifLog


class NiPropertyProcessor:

    __instance = None
    _b_mesh = None
    _n_block = None

    @staticmethod
    def get():
        """ Static access method. """
        if NiPropertyProcessor.__instance is None:
            NiPropertyProcessor()
        return NiPropertyProcessor.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if NiPropertyProcessor.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            super().__init__()
            NiPropertyProcessor.__instance = self

    def register_niproperty(self, processor):
        processor.register(NifFormat.NiMaterialProperty, self.process_nimaterial_property)
        processor.register(NifFormat.NiAlphaProperty, self.process_nialpha_property)
        # processor.register(NifFormat.NiTexturingProperty, self.process_nitexturing_property)
        processor.register(NifFormat.NiStencilProperty, self.process_nistencil_property)
        processor.register(NifFormat.NiSpecularProperty, self.process_nispecular_property)
        processor.register(NifFormat.NiWireframeProperty, self.process_niwireframe_property)
        processor.register(NifFormat.NiVertexColorProperty, self.process_nivertexcolor_property)

    @property
    def b_mesh(self):
        return self._b_mesh

    @b_mesh.setter
    def b_mesh(self, value):
        self._b_mesh = value

    @property
    def n_block(self):
        return self._n_block

    @n_block.setter
    def n_block(self, value):
        self._n_block = value

    def process_nistencil_property(self, prop):
        """Stencil (for double sided meshes"""
        b_mat = self._find_or_create_material()
        Material.set_stencil(b_mat, prop)
        NifLog.debug("NiStencilProperty property processed")

    def process_nispecular_property(self, prop):
        """SpecularProperty based specular"""
        b_mat = self._find_or_create_material()

        # TODO [material][property]
        if NifData.data.version == 0x14000004:
            b_mat.specular_intensity = 0.0  # no specular prop
        NifLog.debug("NiSpecularProperty property processed")

    def process_nialpha_property(self, prop):
        """Import a NiAlphaProperty based material"""
        b_mat = self._find_or_create_material()
        Material.set_alpha(b_mat, prop)
        NifLog.debug("NiAlphaProperty property processed")

    def process_nimaterial_property(self, prop):
        """Import a NiMaterialProperty based material"""
        b_mat = self._find_or_create_material()
        b_mat = NiMaterial().import_material(self.n_block, b_mat, prop)
        # TODO [animation][material] merge this call into import_material
        MaterialAnimation().import_material_controllers(self.n_block, b_mat)
        NifLog.debug("NiMaterialProperty property processed")

    def process_nitexturing_property(self, prop):
        """Import a NiTexturingProperty based material"""
        b_mat = self._find_or_create_material()
        NiTextureProp.get().import_nitextureprop_textures(b_mat, prop)
        NifLog.debug("NiTexturingProperty property processed")

    def process_niwireframe_property(self, prop):
        """Material based specular"""
        b_mat = self._find_or_create_material()
        # todo [material] upgrade needed
        # b_mat.type = 'WIRE'
        NifLog.debug("NiWireframeProperty property processed")

    def process_nivertexcolor_property(self, prop):
        """Material based specular"""
        b_mat = self._find_or_create_material()
        # TODO [property][mesh] Use the vertex color modes
        NifLog.debug("NiVertexColorProperty property processed")

    def _find_or_create_material(self):
        b_mats = self.b_mesh.materials
        if len(b_mats) == 0:
            b_mat = bpy.data.materials.new("")
            # do initial settings for the material here
            b_mat.use_backface_culling = True
            self.b_mesh.materials.append(b_mat)
            NifLog.debug("Created placeholder material to store properties in {0}".format(b_mat))
        else:
            b_mat = self.b_mesh.materials[0]
            NifLog.debug("Reusing existing material {0} to store additional properties in {0}".format(b_mat))
        return b_mat


