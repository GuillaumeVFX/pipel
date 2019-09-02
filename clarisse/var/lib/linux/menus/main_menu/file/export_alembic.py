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

alembic_export_ui_name = "alembic_export_ui"
alembic_export_ui = ix.item_exists("project://default/" + alembic_export_ui_name)
if alembic_export_ui == None:
    alembic_export_ui = ix.create_object(alembic_export_ui_name, "AlembicExportUI", ix.get_item("project://default"))
    alembic_export_ui.set_private(True)
    alembic_export_ui.set_static(True)

if ix.application.inspect(alembic_export_ui, ix.api.AppDialog.cancel(), ix.api.AppDialog.STYLE_OK_CANCEL, "Alembic Export").is_ok():
    options = ix.api.AbcExportOptions(ix.application)

    # Context to be exported
    options.export_mode = ix.api.AbcExportOptions.EXPORT_MODE_CONTEXT
    options.context = ix.get_current_context()

    # Output Alembic file
    options.filename = ix.api.CoreString(alembic_export_ui.get_attribute("filename").get_string())

    # Frame range to be exported
    options.frame_range_mode = ix.api.AbcExportOptions.FRAME_RANGE_MODE_CUSTOM_RANGE
    options.frame_range[0] = alembic_export_ui.get_attribute("frame_range").get_long(0)
    options.frame_range[1] = alembic_export_ui.get_attribute("frame_range").get_long(1)

    # Write one per frame per file : true/false
    options.export_one_frame_per_file = alembic_export_ui.get_attribute("write_one_frame_per_file").get_bool()

    # Transfer data from source Alembic to the output Alembic: true/false
    options.transfer_source_data = alembic_export_ui.get_attribute("transfer_source_data").get_bool()

    # Export combiners: true/false
    options.export_combiners = alembic_export_ui.get_attribute("export_combiners").get_bool()

    # Export scatterers: true/false
    options.export_scatterers = alembic_export_ui.get_attribute("export_scatterers").get_bool()

    # Scatterers export mode: as geometries, or as bounding boxes
    options.scatterer_export_mode = alembic_export_ui.get_attribute("scatterer_export_mode").get_long()

    # Properties option
    options.export_properties = alembic_export_ui.get_attribute("export_properties").get_bool()
    options.fill_sparse_properties = alembic_export_ui.get_attribute("fill_sparse_properties").get_bool()

    ix.api.IOHelpers.export_to_alembic(options)
