#
# Copyright (C) 2009 - 2015 Isotropix SAS. All rights reserved.
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

## @package process_uv_bake
# This file defines a clarisse Process script class used to bake uvs in batch.
#
# It supports UDIM, image sequence output and UV edge padding.
# The script declares two new classes:
# - ProcessUvBake which defines the engine to bake the uvs
# - UvBakeLayer which serves as settings to setup a layer of uv bake 
#   on a specific geometry
#
# The script needs a 3D Layer to be referenced. This 3D Layer is the
# rendering context during the bake. By rendering context understand what defines 
# lights, visibility, aovs etc... 
#
# How it works?
# -------------
# The script instanciates the source image which contains the specified 3D Layer.
# It then disables all other layers of the instance. Using the UvBakeLayer that
# the user has set, the instance is modified to match settings such as
# resolution etc...This image is then rendered along all its AOVs. 
# The resulting is then feed to a new image (matching the resolution) having 
# a Image Layer referencing the render. The script iterates through each 
# rendered AOVs, save the resulting image by applying a LUT and UV edge padding
# if requested.

import math, time

# Definition of the UvBakeLayer class that will be embedded in geometries
uv_bake_layer_cid = '''
class "UvBakeLayer" "ProjectItem" {
    #version 0.9
    embedded_only yes
    attribute_group "baking" {
        reference "uv_slot" {
            null_label "Use First Available"
            filter "UvSlot"
            context "project://default"
            doc "Define which UV slot is used for the baking."
        }
        double[4] "uv_range" {
            value 0.0 0.0 1.0 1.0
            ui_range yes -10.0 10.0
            doc "Set the UV window to use for the baking (left, bottom, right, top)."
        }
        bool "enable_UDIM_baking" {
            value no
            doc "When enabled, the UV range will be splitted into UDIM tiles and the baking will create one file per tile."
        }
        long "eye_direction" {
            value 0
            preset "Normal" "0"
            preset "Camera" "1"
            doc "Set the direction of the eye for the baking."
        }
        long "projection_mode" {
            value 0
            preset "Disabled" "0"
            preset "Inside" "1"
            preset "Outside" "2"
            preset "Inside & Outside" "3"
            doc "Specify the mode of the projection baking. If set to Outside the ray will be launched along the normal and bake the first hit surface. When set to Inside, the ray will be launched in the inverse direction of the normal."
        }
        long "projection_normal" {
            value 1
            preset "Flat" "0"
            preset "Smooth" "1"
            doc "Specify which normal it should use to launch the ray from."
        }
        distance "projection_offset" {
            value 0.0
            ui_range yes 0.0 1.0
            numeric_range_min yes 0.0
            texturable yes
            animatable yes
            doc "Distance from which the ray is launched from the geometry."
        }
        distance "projection_distance" {
            value 0.0
            ui_range_min yes 0.0
            numeric_range_min yes 0.0
            texturable yes
            animatable yes
            doc "Maximum distance to look for another geometry. When set to 0, the distance is infinite."
        }
        pixel "uv_edge_padding" {
            value 0
            ui_range_min yes 0
            doc "Set if the number of pixel to expand around the baked geometry. This filter is also known as a dilation filter."
        }
    }
    attribute_group "image" {
        pixel[2] "resolution" {
            value 512 512
            numeric_range yes 20 16384
            ui_range yes 20 16384
            animatable yes
            doc "Defines the canvas size of the image. The canvas is the visible area of the image."
        }
        enum "LUT" {
            filter "color_space"
            doc "Select the gamma correction you wish to apply to the output image."
        }
        bool "apply_LUT_on_aovs" {
            value 0
            doc "Set if the specified LUT should be applied to AOVs"
        }
        frame "first_frame" {
            value 1
            doc "Set the first output render frame range. If set to 10, the rendering of the image will start at frame 10."
        }
        frame "last_frame" {
            value 1
            doc "Set the last output render frame range. If set to 20, the rendering of the image will stop at frame 20."
        }
        frame "frame_step" {
            value 1
            ui_range yes 1 10
            numeric_range yes 1 1000000
            doc "Set the output render frame step. The frame step is simply the frame increment between two renders in the frame range defined by first and last frame."
        }
        filename_save "save_as" {
            doc "Set the image output filename. The frame number isn't automatically appended to the image name. It must be specified using # character. For example, /path/to/my/bake.####.png will resolve to /path/to/my/bake.0001.png, /path/to/my/bake.0002.png... When enabling UDIM make sure to add the tag <UDIM> in the filename. During rendering the <UDIM> will be replaced by the proper UDIM naming convention"
        }
        long "format" {
            value 0
            doc "Image output fileformat. The image file format ".png" is automatically appended at the end of the image name."
        }
    }
}
'''

# Definition of the UvBakeScriptUi class that is used for UV Baker script UI
uv_baker_script_ui_cid = '''
class "UvBakerScriptUi" "UvBakeLayer" {
    #version 0.9
    abstract yes
    attribute_group "baking" {
        reference "layer_3d" {
            filter "Layer3d"
            doc "Define which 3D layer to use as rendering context (lights, geometries) for the baking."
        }
}
'''

# Return a dictionnary for which keys are all keyframes to be rendered and
# values a vector of images/layers
def get_sequence(geometry_list):
    seq = {}
    layer_list = {}
    img_count = 0

    range_start = range_end = range_step = 0
    for layer in geometry_list:
        layer_name = layer.layer_info.get_full_name()
        # filtering existing layers
        if layer_name in layer_list:
            continue

        range_start = layer.layer_info.attrs.first_frame[0]
        range_end = layer.layer_info.attrs.last_frame[0]
        range_step = layer.layer_info.attrs.frame_step[0]
        if range_start > range_end:
            t = range_start
            range_start = range_end
            range_end = t
        print range_start, range_end, range_step

        for i in range(range_start, (range_end + 1), range_step):
            if i in seq:
                seq[i].add(layer.layer_info)
                img_count += 1
            else:
                layers = []
                layers.append(layer)
                img_count += 1
                seq[i] = layers
        layer_list[layer_name] = True
    return seq, img_count

# helper function that copies values of an attribute to another
def copy_attr(dst, src):
    values = ix.api.CoreStringArray()
    src.get_values(values)
    dst.set_string(values)

# return a formatted padding
def get_padding(padding):
    return '{0:0' + str(padding) + 'd}'

# format a filename so it is expandable in Python for a given frame number
def format_filename(filename):
    sfilename = filename.split('#')
    lsfilename = len(sfilename)
    # uncomment the following block of code to make sure the generated filename
    # always return a valid sequence
    '''
    if lsfilename == 0: return get_padding(5)
    elif lsfilename == 1: return filename + get_padding(5)
    '''
    
    prev = res = ''
    padding = 0
    for entry in sfilename:
        padding += 1
        if entry != '':
            if res != '': res += get_padding(padding)
            elif prev == '' and padding > 1: res += get_padding(padding - 1)
            res += entry
            padding = 0

        prev = entry

    if padding > 0: res += get_padding(padding)
    return res

# render the specified image and stop evaluation when the 
# user aborts the running process
def render_image(image, progress):
    if image.get_module().is_image_dirty(ix.api.ModuleImage.QUALITY_FULL):
        image.get_module().compute_image(ix.api.ModuleImage.QUALITY_FULL, ix.api.ModuleImage.QUALITY_FULL)

    st_time = time.time()
    check_time = 0.03
    # first wait for the image to be computed
    while image.get_module().is_image_dirty(ix.api.ModuleImage.QUALITY_FULL):
        ix.application.wait_for_events()
        if (time.time() - st_time) > check_time:
            # update progress bar
            progress_level = (image.get_module().get_progress() - 0.5) * 2
            progress.set_value(progress_level)
            
        if progress.must_abort():
            image.get_module().stop_compute_image()
            ix.application.stop_evaluation(True)
            return

    # then wait until the evaluation is stopped
    while ix.application.is_evaluating():
        ix.application.wait_for_events()
        if (time.time() - st_time) > check_time:
            # update progress bar
            progress_level = (image.get_module().get_progress() - 0.5) * 2
            progress.set_value(progress_level)
            
        if progress.must_abort():
            image.get_module().stop_compute_image()
            ix.application.stop_evaluation(True)
            return

    return image.get_module().get_image(ix.api.ModuleImage.QUALITY_FULL)

# render and save the specified image with its aovs
def render(filename, image, progress, format, lut_name, aov_image, aov_layer, aovs, aov_lut):
    progress.begin_task('Baking UV Map', 0.75)
    render = render_image(image, progress)
    progress.end_task()
    if render != None: 
        # saving beauty
        aov_layer.get_attribute("output_layer").set_string('rgba')
        progress.begin_task('Rendering \'rgba\'', 0.25 / (len(aovs) + 1))
        aov_render = render_image(aov_image, progress)
        ix.save_image(aov_render, filename, format, lut_name)
        progress.end_task()
        for aov in aovs:
            aov_layer.get_attribute("output_layer").set_string(aov)
            # use alpha from beauty
            aov_layer.get_attribute('alpha_channel').set_long(1)
            aov_layer.get_attribute('custom_channel_name').set_string('rgba.alpha')
            progress.begin_task('Rendering \'' + aov + '\'', 0.25 / (len(aovs) + 1))
            aov_render = render_image(aov_image, progress)
            if aov_render != None: 
                ix.save_image(aov_render, filename + '.' + aov, format, lut_name if aov_lut  else 'linear')
                progress.end_task()
            else:
                return False
                progress.end_task()
        return True
    return False

# bake the UVs with the given image and layer
def bake_uvs(image, layer, aov_image, aov_layer, aovs, edge_padding, geometry, settings, progress):
    # Setting up stuffs...
    current_frame = int(ix.application.get_factory().get_time().get_current_frame())
    lut_name = settings.get_attribute('LUT').get_applied_preset_label().split('|')[-1]
    
    # check if LUT is invalid in that case we assume scene role linear
    if ix.api.ColorIO.get_color_space_index(lut_name) == 0xFFFFFFFF:
        lut_name = ix.api.ColorIO.get_ROLE_SCENE_LINEAR()
        
    layer.get_attribute('uv_bake_geometry').set_object(geometry)
    copy_attr(image.get_attribute('resolution'), settings.get_attribute('resolution'))
    copy_attr(aov_image.get_attribute('resolution'), settings.get_attribute('resolution'))
    
    copy_attr(layer.get_attribute('uv_bake_slot'), settings.get_attribute('uv_slot'))
    copy_attr(layer.get_attribute('uv_bake_eye_direction'), settings.get_attribute('eye_direction'))
    copy_attr(layer.get_attribute('uv_bake_projection_mode'), settings.get_attribute('projection_mode'))
    copy_attr(layer.get_attribute('uv_bake_projection_normal'), settings.get_attribute('projection_normal'))
    copy_attr(layer.get_attribute('uv_bake_projection_offset'), settings.get_attribute('projection_offset'))
    copy_attr(layer.get_attribute('uv_bake_projection_distance'), settings.get_attribute('projection_distance'))
    save_as_attr = settings.get_attribute('save_as')
    uv_range_attr = settings.get_attribute('uv_range')
    format = settings.get_attribute('format').get_long()
    aov_lut = settings.get_attribute('apply_LUT_on_aovs').get_bool()
    
    edge_padding.get_attribute('pixel').set_long(settings.get_attribute('uv_edge_padding').get_long())
    
    if settings.get_attribute('enable_UDIM_baking').get_bool() == True:
        save_as = save_as_attr.get_string()
        min_u = max(0.0, math.floor(uv_range_attr.get_double(0)))
        min_v = max(0.0, math.floor(uv_range_attr.get_double(1)))
        max_u = max(1.0, math.ceil(uv_range_attr.get_double(2)))
        max_v = max(1.0, math.ceil(uv_range_attr.get_double(3)))
        tile_count = (max_u - min_u) * (max_v - min_v)

        save_as_attr = image.get_attribute('save_as')
        uv_range_attr = layer.get_attribute('uv_bake_range')
        v = min_v
        while v < max_v - 0.5:
            uv_range_attr.set_double(v, 1)
            uv_range_attr.set_double(v + 1.0, 3)
            u = min_u
            while u < max_u - 0.5:
                uv_range_attr.set_double(u, 0)
                uv_range_attr.set_double(u + 1.0, 2)
                udim = "%d" % (1001 + int(u) + 10 * int(v))
                save_as_udim = save_as
                if len(save_as) > 0:
                    save_as_udim = save_as.replace('<UDIM>', udim)
                    if save_as_udim == save_as:
                        save_as_udim = save_as + udim + '_' # append a '_' in order to separate it from the frame number
                save_as_attr.set_string(save_as_udim)
                progress.begin_task("Processing tile '%s'" % udim, 1.0 / tile_count)
                # generating current filename from the current frame
                filename = format_filename(save_as_udim).format(current_frame)
                # rendering actual image
                result = render(filename, image, progress, format, lut_name, aov_image, aov_layer, aovs, aov_lut)
                if result == False:
                    print "Aborted..."
                    progress.end_task()
                    return
                progress.end_task()
                u = u + 1.0
            v = v + 1.0
    else:
        copy_attr(layer.get_attribute('uv_bake_range'), uv_range_attr)
        filename = format_filename(save_as_attr.get_string()).format(current_frame)
        # rendering actual image
        result = render(filename, image, progress, format, lut_name, aov_image, aov_layer, aovs, aov_lut)
        if result == False:
            print "Aborted..."
            return

class UvBakeLayer:
    def __init__(self, geometry, layer_info):
        self.geometry = geometry
        self.layer_info = layer_info

# build geometry list from Uv Bake Process
def build_geometry_list(process):
        geometry_list = []
        geometries = process.get_attribute('geometries')
        for i in range(geometries.get_value_count()):
            geom = geometries[i]
            if geom == None: continue
            uv_bake_layers_attr = geom.get_attribute('uv_bake_layers')
            for j in range(uv_bake_layers_attr.get_value_count()):
                uv_bake_layer = uv_bake_layers_attr.get_object(j)
                if uv_bake_layer != None:
                    if uv_bake_layer.get_attribute("save_as").get_string() != "": 
                        geometry_list.append(UvBakeLayer(geom, uv_bake_layer))
                        
        return geometry_list

def run_bake(host_object, ref_layer, geometries, progress):
        if ref_layer == None:
            ix.log_warning("UV Baker: Nothing to do...")
            return False

        # count the number of UV to bake
        if len(geometries) == 0:
                ix.log_warning("UV Baker: Nothing to do...")
                return False

        # create a render process and an instance of the image
        ref_image = ref_layer.get_parent()
        bake_image = host_object.add_embedded_object('image', 'Image', ref_image)
        bake_image.set_static(True)
        bake_image.set_private(True)
        bake_layer = None
        bake_aov_image = host_object.add_embedded_object('aov_image', 'Image')
        bake_aov_layer = bake_aov_image.get_module().add_layer('LayerImage', 'image').get_object()
        edge_padding = bake_aov_layer.get_module().add_filter('ImageFilterUVEdgePadding', 'uv_edge_padding').get_object()
        bake_aov_layer.attrs.image = bake_image

        # clean the instance of the image by removing useless layers
        # and retrieve the layer to use for the baking
        image_layers_attr = bake_image.get_attribute('layers')
        image_layers_attr.localize(True)
        remove_indices = [0]
        for i in range(image_layers_attr.get_value_count()):
            layer = image_layers_attr.get_object(i)
            if layer == None: continue
            if layer.get_source() == ref_layer:
                bake_layer = layer
            else:
                remove_indices.append(i)
        remove_indices[0] = len(remove_indices) - 1 # the first value of the array must be the number of elements
        ix.cmds.RemoveValue([image_layers_attr.get_full_name()], remove_indices)

        bake_image.get_attribute('resolution_multiplier').set_long(2)
        bake_aov_image.get_attribute('resolution_multiplier').set_long(2)
        bake_layer.get_attribute('enable_uv_bake').set_bool(True)
        # setup groups so we get exact same items/lights
        bake_layer.get_attribute('lights').set_object(ref_layer.get_module().get_light_group().get_object())
        bake_layer.get_attribute('geometries').set_object(ref_layer.get_module().get_scene_object_group().get_object())
        bake_layer.get_attribute('shadows').set_object(ref_layer.get_module().get_shadow_object_group().get_object())
        bake_layer.get_attribute('raytracing').set_object(ref_layer.get_module().get_raytraced_object_group().get_object())
        bake_layer.get_attribute('global_illumination').set_object(ref_layer.get_module().get_global_illumination_object_group().get_object())

        # building AOV list from the layer
        
        aovs = []
        aov_list = bake_layer.get_attribute("selected_aov_list")
        enabled_aov_list = bake_layer.get_attribute("enabled_aov_list")
        for i in range(aov_list.get_value_count()):
            if enabled_aov_list.get_bool(i):
                aovs.append(aov_list.get_string(i))

        # getting the sequence to render
        rendering_sequence, img_count = get_sequence(geometries)
        bake_progress_scale = 1.0 / img_count
        current_frame = ix.application.get_factory().get_time().get_current_frame()
        for k in sorted(rendering_sequence):
            if progress.must_abort():
                break
            # set current frame
            ix.application.get_factory().get_time().set_current_frame(k)
            print "Setting current frame to", k

            for settings in rendering_sequence[k]:
                if not progress.must_abort():
                    print "Baking UV for '%s'" % settings.geometry.get_full_name()
                    progress.begin_task(bake_progress_scale)
                    bake_uvs(bake_image, bake_layer, bake_aov_image, bake_aov_layer, aovs, edge_padding, settings.geometry,settings.layer_info, progress)
                    progress.end_task()
                else:
                    break
            
        # delete the instance of the image
        host_object.remove_embedded_object('image')
        host_object.remove_embedded_object('aov_image')
        ix.application.get_factory().get_time().set_current_frame(current_frame)
        return True


# Engine of the ProcessUvBake
class UvBakerScript(ix.api.ModuleProcessScriptEngine):
    def __init__(self):
        ix.api.ModuleProcessScriptEngine.__init__(self)
        
    def declare_attributes(self, cls):
        layer_attr = cls.add_attribute('layer_3d', ix.api.OfAttr.TYPE_REFERENCE, ix.api.OfAttr.CONTAINER_SINGLE, ix.api.OfAttr.VISUAL_HINT_DEFAULT)
        layer_attr_filters = ix.api.CoreStringArray(1)
        layer_attr_filters[0] = 'Layer3d'
        layer_attr.set_object_filters(layer_attr_filters)
        uv_bake_layer_attr = cls.add_attribute('uv_bake_layer', ix.api.OfAttr.TYPE_REFERENCE, ix.api.OfAttr.CONTAINER_SINGLE, ix.api.OfAttr.VISUAL_HINT_DEFAULT)
        uv_bake_layer_attr_filters = ix.api.CoreStringArray(1)
        uv_bake_layer_attr_filters[0] = 'UvBakeLayer'
        uv_bake_layer_attr.set_object_filters(uv_bake_layer_attr_filters)

    def run(self, object, options, progress):
        if  ix.selection.get_count() <= 0 or not ix.selection[0].is_kindof('SceneObject'):
            ix.log_warning("UV Baker: No Scene Object selected...") 
            return False
        bake_layer = object.get_attribute('uv_bake_layer').get_object()
        ref_layer = object.get_attribute('layer_3d').get_object()
        if ref_layer == None:
            ix.log_warning("UV Baker: No 3D Layer selected!") 
            return False
        else:
            geometry_list = []
            geometry_list.append(UvBakeLayer(ix.selection[0], bake_layer))
            return run_bake(object, ref_layer, geometry_list, progress)

# Engine of the ProcessUvBake
class ProcessUvBake(ix.api.ModuleProcessScriptEngine):
    def __init__(self):
        ix.api.ModuleProcessScriptEngine.__init__(self)

    def declare_attributes(self, cls):
        layer_attr = cls.add_attribute('reference_layer', ix.api.OfAttr.TYPE_REFERENCE, ix.api.OfAttr.CONTAINER_SINGLE, ix.api.OfAttr.VISUAL_HINT_DEFAULT)
        layer_attr_filters = ix.api.CoreStringArray(1)
        layer_attr_filters[0] = 'Layer3d'
        layer_attr.set_object_filters(layer_attr_filters)
        geometries_attr = cls.add_attribute('geometries', ix.api.OfAttr.TYPE_REFERENCE, ix.api.OfAttr.CONTAINER_LIST, ix.api.OfAttr.VISUAL_HINT_DEFAULT)
        geometries_attr_filters = ix.api.CoreStringArray(1)
        geometries_attr_filters[0] = 'SceneObject'
        geometries_attr.set_object_filters(geometries_attr_filters)
        self.add_action(cls, 'clear_all')

    def on_action(self, action, object, data):
        if action.get_name() == 'clear_all':
            # removes all references to geometries and all UV bake layers in referenced geometries
            geometries_attr = object.get_attribute('geometries')
            attrs = []
            for i in range(geometries_attr.get_serialized_value_count()):
                geom = geometries_attr.get_serialized_object(i)
                geom_layers_attr = geom.get_attribute('uv_bake_layers')
                if geom_layers_attr:
                    attrs.append(geom_layers_attr.get_full_name())
            attrs.append(geometries_attr.get_full_name())
            ix.cmds.RemoveAllValues(attrs)

    def on_attribute_change(self, object, attr, dirtiness, dirtiness_flags):
        attr_evt = attr.get_event_info()
        if attr.get_name() == 'geometries' and attr_evt.type != ix.api.OfAttrEvent.TYPE_PROPAGATE:
            for i in range(attr.get_value_count()):
                obj = attr.get_object(i)
                if obj == None: continue
                # add a uv_bake_layers attribute to reference geometries if it doesn't exist already
                layers_attr = obj.attribute_exists('uv_bake_layers')
                if layers_attr == None:
                    layers_attr = obj.add_attribute('uv_bake_layers', ix.api.OfAttr.TYPE_OBJECT, ix.api.OfAttr.CONTAINER_ARRAY, ix.api.OfAttr.VISUAL_HINT_DEFAULT, 'uv_bake')
                    layers_attr.set_dg_active(False)
                    layers_attr_filters = ix.api.CoreStringArray(1)
                    layers_attr_filters[0] = 'UvBakeLayer'
                    layers_attr.set_object_filters(layers_attr_filters)

    def run(self, object, options, progress):
        ref_layer = object.get_attribute('reference_layer').get_object()
        return run_bake(object, ref_layer, build_geometry_list(object), progress)

object_factory = ix.application.get_factory()
class_factory = object_factory.get_classes()

# Create the UvBakeLayer class
uv_bake_layer_class = class_factory.exists('UvBakeLayer')
if uv_bake_layer_class == None:
    uv_bake_layer_class = class_factory.add_from_cid(uv_bake_layer_cid)
    format_attr = uv_bake_layer_class.get_attribute('format')
    for i in range(ix.api.ImageIOFileFormat.SAVE_COUNT):
        format = ix.api.ImageIOFileFormat.get_save_name(i);
        value = '%d' % i
        format_attr.add_preset(format, value);
    cs_enum = object_factory.get_enum('color_space')
    if cs_enum != None and cs_enum.get_value_count() != 0:
        lut_attr = uv_bake_layer_class.get_attribute('LUT')
        lut_attr.set_string(cs_enum.get_label(0))
    uv_bake_script_ui_class = class_factory.add_from_cid(uv_baker_script_ui_cid)
    print "UvBakeLayer class successfully added."
else:
    print "UvBakeLayer class already exists."

# Register the UvBakeScript
if ix.api.ModuleProcessScript.register_scripted_process(ix.application, 'UvBakerScript', UvBakerScript()):
    print "UvBakeScript successfully registered."
else:
    print "An error occurred while registring UvBakeScript"

# Register the ProcessUvBake
if ix.api.ModuleProcessScript.register_scripted_process(ix.application, 'ProcessUvBake', ProcessUvBake()):
    print "ProcessUvBake successfully registered."
else:
    print "An error occurred while registring ProcessUvBake"

