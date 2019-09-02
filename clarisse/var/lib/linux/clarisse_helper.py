
## @package clarisse_helper
# This module defines to python Clarisse function helpers.
#
# The file is automatically imported directly inside the ix module.
# To acess to the functions just type for example: ix.render_image('my_image')

import ix
import os

## Load the specified Clarisse project file.
# @param filename Clarisse project filename
# Loading a project will clear all the items that are in the current project.
def load_project(filename):
    application.load_project(filename)
    if not is_gui_application():
        application.set_current_project_filename(filename)

## Save the current project
# @param filename Clarisse project filename
def save_project(filename):
    application.save_project(filename)

## Export the current project as render archive.
# @param filename Clarisse render archive filename
# @return true if the render archive has been successfully exported.
# @note this function can only be called from within an interactive Clarisse session.
def export_render_archive(filename):
    return application.export_render_archive(filename)

## Render the specified image item and return the rendered image.
# @param image Clarisse path to an image item that can be either a string or an OfObject
# @return The rendered image is returned as an ImageHandle
def render_image(image):
    cimg = image
    if isinstance(image, str): cimg = get_item(image)
    if not isinstance(cimg.get_module(), api.ModuleImage):
        raise RuntimeError('the specified item isn\'t an Image')

    if cimg.get_module().is_image_dirty(api.ModuleImage.QUALITY_FULL):
        cimg.get_module().compute_image(api.ModuleImage.QUALITY_FULL, api.ModuleImage.QUALITY_FULL)

    # first wait for the image to be computed
    while cimg.get_module().is_image_dirty(api.ModuleImage.QUALITY_FULL):
        application.wait_for_events()

    # then wait until the evaluation is stopped
    while application.is_evaluating():
        application.wait_for_events()

    return cimg.get_module().get_image(api.ModuleImage.QUALITY_FULL)

## @defgroup python_image_savers Python Image Savers
# This set of function helpers allows you to save Clarisse images in Python

## Save the specified image at the specified filename with the specified format and return True if sucessful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param format Saved file format. Supported formats are defined in the ImageIOFileFormat::Save enum.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @param compression -- Compression mode (for openexr only). Default is no compression.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_image(image, filename, format, lut_name="", compression = 1):
    if isinstance(image, api.ImageHandle): image = image.get_canvas()
    elif not isinstance(image, api.ImageCanvas): raise TypeMismatch("expecting class ImageHandle or ImageCanvas for image argument")
    return api.IOHelpers.save_image(application, image, filename, format, lut_name, compression)

## Save the specified image at the specified filename as a 16-bit (float) EXR. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @param compression -- Compression mode (for openexr only). Default is no compression.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_exr16(image, filename, lut_name="", compression = 1):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_OPEN_EXR_16, lut_name, compression)

## Save the specified image at the specified filename as a 32-bit (float) EXR. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @param compression -- Compression mode (for openexr only). Default is no compression.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_exr32(image, filename, lut_name="", compression = 1):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_OPEN_EXR_32, lut_name, compression)

## Save the specified image at the specified filename as a JPG. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_jpg(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_JPEG, lut_name)

## Save the specified image at the specified filename as a BMP. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_bmp(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_BITMAP, lut_name)

## Save the specified image at the specified filename as a TGA. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving..
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_tga(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_TARGA, lut_name)

## Save the specified image at the specified filename as a 8-bit PNG. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_png8(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_PNG_8, lut_name)

## Save the specified image at the specified filename as a 16-bit PNG. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_png16(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_PNG_16, lut_name)

## Save the specified image at the specified filename as a 8-bit TIF. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving..
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_tif8(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_TIFF_8, lut_name)

## Save the specified image at the specified filename as a 16-bit TIF. Return True if successful.
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_tif16(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_TIFF_16, lut_name)

## Save the specified image at the specified filename as a 32-bit TIF. Return True if successful
# @param image image to be saved (ImageHandle or ImageCanvas).
# @param filename Saved image path string without image format extension.
# @param lut name -- By default, "sRGB" lut is applied to the image prior saving.
# @return The rendered image is returned as an ImageHandle
# @ingroup python_image_savers
def save_tif32(image, filename, lut_name=""):
    return save_image(image, filename, api.ImageIOFileFormat.SAVE_TIFF_32, lut_name)

## Return the current frame number
def get_current_frame():
    return application.get_factory().get_time().get_current_frame()

## Set the current frame number to the specified frame.
# @param frame_number Frame number.
def set_current_frame(frame_number):
    application.get_factory().get_time().set_current_frame(float(frame_number))

## Return a OfObject if the specified geometry has been successfully loaded.
# @param filename Geometry filename.
# @note A single geometry file can define multiple geometries. This is why this function returns an OfObject
def import_geometry(filename):
    object = 0
    objects = api.OfObjectVector()
    api.IOHelpers.import_geometry(application, filename, objects)
    if objects.get_count() > 0:
        object = objects[0]
    else:
        application.log_error('Failed to import \'' + filename +'\' geometry.')

    return object

## Return an array of OfObject if the specified geometry has been successfully loaded.
# @param filenames Geometry filenames.
# @note A single geometry file can define multiple geometries. This is why this function returns a array of OfObject
def import_geometries(filenames):
    objects = api.OfObjectVector()
    api.IOHelpers.import_geometries(application, filenames, objects)
    return objects

## Return a OfObject if the specified image has been successfully loaded.
# @param filename Image filename.
def import_image(filename):
    object = 0
    api.IOHelpers.import_image(application, filename, object)
    return object

## Return an array of OfObject if the specified images has been successfully loaded.
# @param filenames Images filenames.
def import_images(filenames):
    objects = api.OfObjectVector()
    api.IOHelpers.import_images(application, filenames, objects)
    return objects

## Return a OfObject if the specified image has been successfully loaded.
# @param filename Image filename.
# @param class_name Class name.
# @param suffix Suffix object created.
def import_map_file(filename, class_name, suffix):
    object = 0
    api.IOHelpers.import_texture(application, filename, class_name, suffix, object)
    return object

## Return an array of OfObject if the specified images has been successfully loaded.
# @param filenames Images filenames.
# @param class_name Class name.
# @param suffix Suffix object created.
def import_map_files(filenames, class_name, suffix,):
    objects = api.OfObjectVector()
    api.IOHelpers.import_textures(application, filenames, class_name, suffix, objects)
    return objects

## Return a OfObject if the specified volume has been successfully loaded.
# @param filename Volume filename.
# @note A single volume file can define multiple volumes. This is why this function returns the created context containing the volume
def import_volume(filename):
    return api.IOHelpers.import_volume(application, filename)

## Return an array of OfObject if the specified volumes has been successfully loaded.
# @param filenames Volume filenames.
# @note A single volume file can define multiple volumes. This is why this function returns the created context containing the volume
def import_volumes(filenames):
    return api.IOHelpers.import_volumes(application, filenames)

## Exports the geometry given as parameter
# @param filename output Geometry filename.
# @param geometry_object to export
def export_geometry(filename, geometry_object):
    vec = api.OfObjectVector()
    vec.add(geometry_object)
    api.IOHelpers.export_geometry(application, filename, vec)

## Exports the geometry given as parameter
# @param filename output Geometry filename
# @param OfObjectVector vector of Geometries to export
# @note A single geometry file can define multiple geometries.
def export_geometries(filename, geometry_objects):
    if type(geometry_objects) is list:
        vec = ix.api.OfObjectVector()
        for geo in geometry_objects:
            vec.add(geo)
        api.IOHelpers.export_geometry(application, filename, vec)
    elif geometry_objects.get_count() > 0:
        api.IOHelpers.export_geometry(application, filename, geometry_objects)
    else:
        raise RuntimeError('Failed to export: geometry_objects is empty.')

## When a single file is specified, return the OfContext that has been successfully referenced. When an array of filenames is specified, returns True in case of success.
# @param working_context Context that will contain the referenced asset
# @param filename Asset filename(s)
def reference_file(working_context, filename):
    return api.IOHelpers.reference_file(working_context, filename)

## Return an array of OfContexts if the specified files have been successfully referenced.
# @param working_context Context that will contain the referenced assets
# @param filenames Asset filenames
def reference_files(working_context, filenames):
    refs = api.OfContextVector()
    api.IOHelpers.reference_files(working_context, filenames, refs)
    return refs

## Export a context to the specified project filename
# @param app Application object
# @param context Context
# @param filename project filename
def export_context_as_project(context, filename):
    api.IOHelpers.export_context_as_project(application, context, filename)

## Export a context to the specified project filename, including its dependencies
# @param app Application object
# @param context Context
# @param filename project filename
def export_context_as_project_with_dependencies(context, filename):
    api.IOHelpers.export_context_as_project_with_dependencies(application, context, filename)

## Export a context to the specified project filename
# @param app Application object
# @param context Context
# @param filenames project filename
def reference_export_context(context, filename):
    api.IOHelpers.reference_export_context(application, context, filename)

## Make local object from the specified a reference
# @param app Application object
# @param context Context that will a local context
def reference_make_local(context):
    api.IOHelpers.reference_make_local(application, context)

## Return the created context containing the scene if the specified file has been successfully loaded.
# @param filename Scene filename.
def import_scene(filename):
    context = api.IOHelpers.import_scene(application, filename)
    if context == None:
        application.log_error('Failed to import \'' + filename +'\' scene.')
    return context

## Return the created context containing the scene if the specified file has been successfully loaded.
# @param filename Scene filename.
def import_project(filename):
    context = api.IOHelpers.import_project(application, filename)
    if context == None:
        application.log_error('Failed to import \'' + filename +'\' scene.')
    return context

## Output the specified info message
# @param message input message
def log_info(message):
    application.log_info(str(message))

## Output the specified warning message
# @param message input message
def log_warning(message):
    application.log_warning(str(message))

## Output the specified error message and raise an error
# @param message input message
def log_error(message):
    application.log_error(str(message))
    raise RuntimeError

## Return True if the application is running in GUI mode
# Use this method if you are doing specific GUI actions to check if the application is running in UI mode.
# Typically Clarisse returns true, where cnode returns false.
def is_gui_application():
    return application.get_type() == api.AppBase.TYPE_GUI

## Return True if the application is running in process mode
# A process application, is an application which doesn't take input.
# Typically cnode returns true when it running as a renderer and will return false if running in interactive mode
def is_process_application():
    return application.get_type() == api.AppBase.TYPE_PROCESS

## Return True if the application is running in interactive mode
# An interactive application, is an application that behaves like a command-line shell.
# Typically cnode returns true when it has been launched with the flag -interactive.
def is_interactive_application():
    return application.get_type() == api.AppBase.TYPE_INTERACTIVE

## Set the current working context (Global slot)
# @param context_path Path the the context that will be set as the current working context
# @note By default all new items are created in the current working context.
def set_current_context(context_path):
    new_context = application.get_factory().context_exists(make_absolute_of_path(context_path));
    if new_context != None:
        application.get_selection().set_slot_working_context("Global", new_context)
    else:
        print "The specified context '" + context_path + "' doesn't exists."

## Return the current working context (OfContext)
def get_current_context():
    return application.get_selection().get_slot_working_context("Global")

## Create an object named item_name of the specified class_name inside the current working context.
# @param item_name Name of the newly created item
# @param class_name Object class name of the item to create
# @param destination_context Destination context in which the object is created. By default, objects are created in the current application context
# @note If the specified item_name already exists, the item will be automatically renamed.
# @return Return the new item (OfObject) on success or None
def create_object(item_name, class_name, destination_context=None):
    if destination_context == None:
         destination_context = get_current_context()
    return destination_context.add_object(item_name, class_name)

## Delete the specified item (object or context)
# @param item Path to the item to delete, for example: 'project://scene/light'
# @note You can't undo this action.
def delete_item(item):
    name = None
    if isinstance(item, str):
        name = make_absolute_of_path(item)
    elif isinstance(item, api.OfItem):
        name = item.get_full_name()
    elif isinstance(item, api.PyOfObject):
        if item.m_object is not None:
            name = item.m_object.get_full_name()
    if name is not None:
        application.get_factory().remove_item(name)

## Return True if the specified context exists
# @param context_name Name of the context,  for example: 'project://scene'
def is_context_exists(context_name):
    return application.get_factory().context_exists(make_absolute_of_path(context_name))

## Return the specified item (OfContext or OfObject) if it exists
# @param item_name Name of the item,  for example: 'project://scene/light'
# @return Return None if the item doesn't exists
def item_exists(item_name):
    path = make_absolute_of_path(item_name)
    ctx = application.get_factory().context_exists(path)
    if ctx != None: return ctx
    else:
        attr = application.get_factory().find_attribute(path)
        if attr != None: return attr
        else:
            obj = application.get_factory().object_exists(path)
            if isinstance(obj, api.PyOfObject):
                if obj.m_object is not None:
                    return obj
                else:
                    return None
            else:
                return obj

## Return the item (OfContext or OfObject) from the specified name
# @param item_name Name of the item to get,  for example: 'project://scene/light'
# @return Return None if it fails to locate the specified item
def get_item(item_name):
    item = item_exists(item_name)
    if item == None: raise LookupError("Failed to find item '" + item_name + "'.")
    return item

## Return the specified path as an absolute Clarisse path (containing project://)
def make_absolute_of_path(path):
    if path[0:9] != 'project:/':
        if path[0] == '/': return 'project:/' + path
        else: return 'project://' + path
    else: return path


def _get_of_object(item):
    object = None
    if isinstance(item, str): object = get_item(item)
    elif isinstance(item, api.OfItem):
        object = item
    elif isinstance(item, api.PyOfObject):
        object = item.m_object
    return object

## Display the attributes of the specified item
def inspect(item):
    object = _get_of_object(item)
    if object is not None:
        application.inspect(object)

## Create a new context
def create_context(path):
    abspath = make_absolute_of_path(path)
    if not is_context_exists(abspath):
        slist = abspath.rsplit('/', 1)
        ctx = is_context_exists(slist[0])
        if ctx is None:
            raise RuntimeError('The specified \'' + slist[0] + '\' doesn\'t exists')
        else:
            a = str(slist[-1])
            return ctx.add_context(a)
    else:
        raise RuntimeError('The specified \'' + abspath + '\' already exists')

## Create and return a new generic object name after the specified name
# @note A generic object doesn't declare any attribute. You can then use it add your custom attributes on it. For example, it's typical use is to create a temporary generic object, populate it with custom attributes. Then you would use inspect to display its attribute to get user input. Once the data as been retreived the object can be freely deleted.
def create_generic_object(object_name):
    return application.get_factory().add_generic_object(object_name)

## Add and return a custom attribute to the specified object
# @param obj Object that will get the new attribute
# @param attr_name New attribute name
# @param attr_type String defining the type of the attribute. Following are the possible attribute type values:
#   - 'bool' to define a boolean (True/False) value
#   - 'long' to define a long value
#   - 'double' to define a double floating point value
#   - 'reference' to define a reference to an object
#   - 'percentage' to define a percentage
#   - 'distance' to define a distance
#   - 'scale' to define a scale
#   - 'angle' to define an angle
#   - 'frame' to define a frame
#   - 'subframe' to define a subframe
#   - 'l' to define a luminance color
#   - 'la' to define a luminance + alpha color
#   - 'rgb' to define a RGB color
#   - 'rgba' to define a RGBA color
#   - 'filein' to define a filein value
#   - 'fileout' to define a fileout value
#   - 'pixel' to define a pixel value
#   - 'subpixel' to define a subpixel value (allowing fractional values)
# @param category User category of the attribute.
# @return The newly created attribute
# @note If the specified attribute name already exists, it will get automatically renamed. Attribute names support only identifier type string: 'my_attribute_name'
def add_attribute(obj, attr_name, attr_type, category = "General"):
    if obj is None: raise ValueError("The specified object is null")
    attr = None
    if  attr_type == "bool": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_BOOL, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_DEFAULT, category)
    elif attr_type == "long": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_LONG, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_DEFAULT, category)
    elif attr_type == "double": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_DEFAULT, category)
    elif attr_type == "string": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_STRING, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_DEFAULT, category)
    elif attr_type == "reference": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_REFERENCE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_DEFAULT, category)
    elif attr_type == "percentage": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_PERCENTAGE, category)
    elif attr_type == "distance": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_DISTANCE, category)
    elif attr_type == "angle": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_ANGLE, category)
    elif attr_type == "scale": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_SCALE, category)
    elif attr_type == "frame": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_LONG, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_FRAME, category)
    elif attr_type == "subframe": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_SUBFRAME, category)
    elif attr_type == "l": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_L, category)
    elif attr_type == "la":
        attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_LA, category)
        attr.set_value_count(2)
    elif attr_type == "rgb":
        attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_RGB, category)
        attr.set_value_count(3)
    elif attr_type == "rgba":
        attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_RGBA, category)
        attr.set_value_count(3)
    elif attr_type == "filein": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_FILE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_FILENAME_OPEN, category)
    elif attr_type == "fileout": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_FILE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_FILENAME_SAVE, category)
    elif attr_type == "pixel": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_PIXEL, category)
    elif attr_type == "subpixel": attr = obj.add_attribute(attr_name, api.OfAttr.TYPE_DOUBLE, api.OfAttr.CONTAINER_SINGLE, api.OfAttr.VISUAL_HINT_SUBPIXEL, category)
    else: raise RuntimeError('Unrecognized attribute type')
    return attr

## Enable command history
def enable_command_history():
    application.get_command_manager().enable_history()

## Disable command history
def disable_command_history():
    application.get_command_manager().disable_history()

## Enable echo command
def enable_echo_command():
    application.get_command_manager().echo_command(True)

## Disable echo command
def disable_echo_command():
    application.get_command_manager().echo_command(False)

## Start new a command batch by pushing it in the batch stack (batches can be nested)
# @param batch_name The name of the command batch that will be displayed in the History Editor
def begin_command_batch(batch_name):
    application.get_command_manager().enable_history()
    application.get_command_manager().begin_batch(batch_name)

## End a command batch by poping it from the batch stack
def end_command_batch():
    application.get_command_manager().end_batch()
    application.get_command_manager().disable_history()

## Check if the current project is modified and proposed to save it
# @return Return the response of file browser and the filename chosen (Can return a None value for the filename)
def check_need_save():
    res = ix.api.AppDialog.cancel()
    app = ix.application
    if app.is_project_modified():
        clarisse_window = app.get_event_window()
        box = ix.api.GuiMessageBox(app, 0, 0, "Isotropix Clarisse: Information", "The current project has changed. Would you like to save changes?", )
        x = (2 * clarisse_window.get_x() + clarisse_window.get_width() - box.get_width()) / 2
        y = (2 * clarisse_window.get_y() + clarisse_window.get_height() - box.get_height()) / 2
        box.resize(x, y, box.get_width(), box.get_height())
        box.set_style(ix.api.AppDialog.STYLE_YES_NO_CANCEL)
        box.show()
        res = box.get_value()
        box.destroy()
        if not res.is_cancelled():
            if res.is_yes():  # save otherwise nothing to do
                current_filename = app.get_current_project_filename()

                project_ext = app.get_project_extension_name()[0]
                if project_ext == "ple" :
                    if current_filename != "":
                        current_filename, ext = os.path.splitext(current_filename)
                        if ext != ("." + project_ext):
                            current_filename = ""

                if current_filename == "": current_filename = "untitled"
                filename = ix.api.GuiWidget.save_file(app, current_filename, "Save Scene File...", "Project Files\t*." + project_ext)
                if filename != "":
                    return ix.api.AppDialog.yes(), filename
                else:
                    res = ix.api.AppDialog.cancel()
        else:
            res = ix.api.AppDialog.cancel()
    else:
        res = ix.api.AppDialog.no()
    return res, None

## Clarisse global application selection class wrapper
class ApplicationSelection:
    ## Allow for subscript operator
    def __getitem__(self, index):
        return self.get(index)

    ## Return True if the selection is empty
    def is_empty(self):
        return self.get_count() == 0

    ## Add the specified item (OfItem) to the selection
    def add(self, item):
        if isinstance(item, basestring):
            item_object = ix.get_item(item)
            if item_object is not None:
                application.get_selection().add_item("global", item_object, "Global")
            else:
                raise RuntimeError("Can't set selection: item does not exist.")
        else:
            application.get_selection().add_item("global", item, "Global")

    ## Return the selected item at the specified index
    def get(self, index):
        if index < application.get_selection().get_count("global"):
                        obj = application.get_selection().get_item("global", index)
                        if obj.is_object():
                                return obj.to_object()
                        else:
                                return obj.to_context()
        else:
            raise IndexError("The index (" + str(index) + ") is out of range")

    ## Return the number of items in the selection
    def get_count(self):
        return application.get_selection().get_count("global")

    ## Deselect all selected items
    def deselect_all(self):
        application.get_selection().remove_all("global", "Global")

    ## Set the selection to the current item
    def select(self, item):
        if type(item) is list or type(item) is ix.api.OfObjectVector  or type(item) is ix.api.OfItemArray:
            self.deselect_all()
            for i in range(item.get_count()):
                if item[i] is not None:
                    self.add(item[i])
        else:
            if item is not None:
                self.deselect_all()
                self.add(item)
            else:
                raise RuntimeError("Can't set selection: item does not exist.")

    ## Select all items
    def select_all(self):
        application.get_selection().select_all("global", "Global")

    ## Get selection objects
    def get_objects(self):
        vec = ix.api.OfObjectVector()
        application.get_selection().get_objects(vec)
        return vec

    ## Get selection contexts
    def get_contexts(self):
        vec = ix.api.OfContextVector()
        application.get_selection().get_contexts(vec)
        return vec

## Global application selection helper
selection = ApplicationSelection()
