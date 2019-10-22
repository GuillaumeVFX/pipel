<?php
/**
 * FooGallery JGWIllGalleryTemplate1910 gallery template
 * This is the template that is run when a FooGallery is rendered to the frontend
 */
//the current FooGallery that is currently being rendered to the frontend
global $current_foogallery;

$lightbox = foogallery_gallery_template_setting( 'lightbox', 'unknown' );
$additional_class_from_setting = foogallery_gallery_template_setting( 'another_setting_id', 'additional_class_from_setting' );
$additional_class = 'additional_class'; //an additional hard-coded class used by the template

$foogallery_default_classes = foogallery_build_class_attribute_safe( $current_foogallery, 'foogallery-lightbox-' . $lightbox, $additional_class, $additional_class_from_setting );
$foogallery_default_attributes = foogallery_build_container_attributes_safe( $current_foogallery, array( 'class' => $foogallery_default_classes ) );

?><div <?php echo $foogallery_default_attributes; ?>>
	<?php foreach ( foogallery_current_gallery_attachments_for_rendering() as $attachment ) {
        //echo foogallery_attachment_html( $attachment );
	} ?>
</div>