# Copyright (C) 2009 - 2016 Isotropix SAS. All rights reserved.
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


import math, time

# Definition of the Alembic Export UI class
ui_export_alembic_cid = '''
class "AlembicExportUI" "ProjectItem" {
#version 0.91
    doc "UI for exporting objects to Alembic."
    abstract yes

    attribute_group "output" {
        filename_save "filename" {
            extension "abc"
        }
    }

    attribute_group "animation" {
        long[2] "frame_range" {
            value 0 1
        }

        bool "write_one_frame_per_file" {
            value no
            doc "When checked, the export process will create one file per frame."
        }

        bool "transfer_source_data" {
            value no
            doc "When checked, Alembic objects will be exported by transferring the original data from the source file to the new one. Unchecking this option will re-bake objects using Clarisse's frame rate, and custom properties will be lost."
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
            doc "When checked, Particle Container properties will be exported as arbGeomparams."
        }

        bool "fill_sparse_properties" {
            value no
            doc "When checked, sparse properties will be filled with a default value (zero). This option must be enabled to be compatible with applications that don't support sparse properties (such as Houdini)."
        }
    }
}
'''

object_factory = ix.application.get_factory()
class_factory = object_factory.get_classes()

# Create the AlembicExportUI class
export_alembic_ui_class = class_factory.exists('AlembicExportUI')
if export_alembic_ui_class == None:
    export_alembic_ui_class = class_factory.add_from_cid(ui_export_alembic_cid)
    print "AlembicExportUI class successfully added."
else:
    print "AlembicExportUI class already exists."
