# Copyright (C) 2009 - 2019 Isotropix SAS. All rights reserved.
#
# The information in this file is provided for the exclusive use of
# the software licensees of Isotropix. Contents of this file may not
# be distributed, copied or duplicated in any form, in whole or in
# part, without the prior written permission of Isotropix SAS.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


#
# Define AbcExportOptionsUi attributes.
#
abc_export_options_ui_cid = '''
    attribute_group "output" {
        filename_save "filename" {
            extension "abc"
        }
    }

    attribute_group "animation" {
        long[2] "frame_range" {
            value 0 0
            doc "Specify the start/end frames to export."
        }

        bool "write_one_frame_per_file" {
            value no
            doc "When checked, the export process will create one file per frame."
        }

        bool "transfer_source_data" {
            value no
            doc "When checked, Alembic objects will be exported by transferring the original data from the source file to the new one. Disabling this option will re-bake objects using Clarisse's frame rate, and custom properties will be lost."
        }
    }

    attribute_group "combiners" {
        bool "export_combiners" {
            value yes
            doc "When checked, combiners will be exported as pivots with their sub-objects as direct children. Sub-combiners are exported recursively."
        }
    }

    attribute_group "scatterers" {
        bool "export_scatterers" {
            value yes
            doc "When checked, scatterers will be exported as a hierarchy of instances, otherwise scatterers and their instances are not exported."
        }

        long "scatterer_export_mode" {
            value 0
            preset "Instances As Geometries" "0"
            preset "Instances As Bounding Boxes" "1"
            doc "When using the Geometries mode, scattered instances are exported as is. When using the Bounding Boxes mode, instances are replaced by their bounding box."
        }
    }

    attribute_group "properties" {
        bool "export_properties" {
            value yes
            doc "When checked, Particle Container properties will be exported. The exported properties are created under the standard Alembic property group .arbGeomParams."
        }

        long "compatibility_mode" {
            value 0
            preset "None" "0"
            preset "Houdini" "1"
            preset "Houdini and Katana" "2"
            doc "Select a preset for the properties options Fill Sparse Properties, Promote To Geometry Parameter and Bake Indexed Properties. Options are editable when using the mode None, otherwise they are read-only with pre-defined values."
        }

        bool "fill_sparse_properties" {
            value no
            doc "When checked, sparse properties will be filled with a default value (zero). This option must be enabled to be compatible with applications that don't support sparse properties (e.g. Houdini)."
        }

        bool "promote_to_geometry_parameter" {
            value yes
            doc "When checked, all properties whose traits (type, size, ...) match Alembic's Typed Geometry Parameters will be exported as Geometry Parameters, and properties that don't match such traits are exported as regular properties. When unchecked, all properties are exported as regular properties. It is recommended to enable this option unless the target application doesn't support Geometry Parameters (e.g. Katana)."
        }

        bool "bake_indexed_properties" {
            value no
            doc "When checked, all indexed properties except Geometry Parameters will be baked as non-sparse array properties: values are unshared and will use more memory and disk space. Enabling this option can improve compatibility with other applications. When unchecked, indexed properties will be exported unchanged (a compound property with 2 children properties: an array of indices and an array of indexed values)."
        }
    }
'''

#
# Scripted class engine for AbcExportOptionsUi.
#
class AbcExportOptionsUiEngine(ix.api.ModuleScriptedClassEngine):

    #
    # Initialize the engine.
    #
    def __init__(self):
        ix.api.ModuleScriptedClassEngine.__init__(self)

    #
    # Handle attribute change.
    #
    def on_attribute_change(self, object, attr, dirtiness, dirtiness_flags):

        if attr.get_name() == "write_one_frame_per_file":
            object.get_attribute("transfer_source_data").set_read_only(attr.get_bool() == True)
            return

        if attr.get_name() == "export_scatterers":
            object.get_attribute("scatterer_export_mode").set_read_only(attr.get_bool() == False)
            return

        if attr.get_name() == "export_properties":
            is_read_only = attr.get_bool() == False
            object.get_attribute("compatibility_mode").set_read_only(is_read_only)
            object.get_attribute("fill_sparse_properties").set_read_only(is_read_only)
            object.get_attribute("promote_to_geometry_parameter").set_read_only(is_read_only)
            object.get_attribute("bake_indexed_properties").set_read_only(is_read_only)
            return

        if attr.get_name() == "compatibility_mode":
            attr_fill = object.get_attribute("fill_sparse_properties")
            attr_promote = object.get_attribute("promote_to_geometry_parameter")
            attr_bake = object.get_attribute("bake_indexed_properties")

            mode = attr.get_long()
            attr_fill.set_bool(ix.api.AbcExportOptions.get_fill_sparse_properties(mode))
            attr_promote.set_bool(ix.api.AbcExportOptions.get_promote_to_geometry_parameter(mode))
            attr_bake.set_bool(ix.api.AbcExportOptions.get_bake_indexed_properties(mode))

            is_read_only = mode != ix.api.AbcExportOptions.PropertiesCompatibilityMode_Default
            attr_fill.set_read_only(is_read_only)
            attr_promote.set_read_only(is_read_only)
            attr_bake.set_read_only(is_read_only)

            return

#
# Register the scripted class and engine.
#
scripted_class_name = 'AbcExportOptionsUi'
if not ix.api.ModuleScriptedClass.register_scripted_class(ix.application, scripted_class_name, AbcExportOptionsUiEngine(), abc_export_options_ui_cid, True):
    ix.log_error('Failed to register class {}: the CID might be invalid or the class might already exist.'.format(scripted_class_name))

#
# Check that class registration is complete.
#
scripted_class = ix.application.get_factory().get_classes().get(scripted_class_name)
if scripted_class and scripted_class.get_attribute_count() > 0:
    ix.log_info('Successfully registered class {}.'.format(scripted_class_name))
else:
    ix.log_error('Incomplete registration of class {}, Alembic export is disabled.'.format(scripted_class_name))
