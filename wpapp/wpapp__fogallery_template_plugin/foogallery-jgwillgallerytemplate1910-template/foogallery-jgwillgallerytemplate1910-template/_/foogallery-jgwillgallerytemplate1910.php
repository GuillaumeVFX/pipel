<?php
/**
 * FooGallery - JGWIllGalleryTemplate1910
 *
 * Une gallerie
 *
 * Plugin Name: FooGallery - JGWIllGalleryTemplate1910
 * Description: Une gallerie
 * Version:     1.0.0
 * Author:      Guillaume Descoteaux-Isabelle
 * Author URI:  http://guillaumeisabelle.com/r/coding
 * License:     GPL-2.0+
 * License URI: http://www.gnu.org/licenses/gpl-2.0.txt
 */

if ( !class_exists( 'FooGallery_JGWIllGalleryTemplate1910_Template' ) ) {

	define('FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_FILE', __FILE__ );
	define('FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL', plugin_dir_url( __FILE__ ));
	define('FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_VERSION', '1.0.0');
	define('FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_PATH', plugin_dir_path( __FILE__ ));
	define('FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_SLUG', 'foogallery-jgwillgallerytemplate1910');

	class FooGallery_JGWIllGalleryTemplate1910_Template {
		/**
		 * Wire up everything we need to run the extension
		 */
		function __construct() {
			add_filter( 'foogallery_gallery_templates', array( $this, 'add_template' ) );
			add_filter( 'foogallery_gallery_templates_files', array( $this, 'register_myself' ) );
			add_filter( 'foogallery_located_template-jgwillgallerytemplate1910', array( $this, 'enqueue_dependencies' ) );
			add_filter( 'foogallery_template_js_ver-jgwillgallerytemplate1910', array( $this, 'override_version' ) );
			add_filter( 'foogallery_template_css_ver-jgwillgallerytemplate1910', array( $this, 'override_version' ) );
			add_filter( 'foogallery_gallery_template_arguments-jgwillgallerytemplate1910', array( $this, 'build_gallery_template_arguments' ) );
		}

		/**
		 * Register myself so that all associated JS and CSS files can be found and automatically included
		 * @param $extensions
		 *
		 * @return array
		 */
		function register_myself( $extensions ) {
			$extensions[] = __FILE__;
			return $extensions;
		}

		/**
		 * Override the asset version number when enqueueing extension assets
		 */
		function override_version( $version ) {
			return FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_VERSION;
		}

		/**
		 * Enqueue any script or stylesheet file dependencies that your gallery template relies on
		 */
		function enqueue_dependencies() {
			//wp_enqueue_script(
			//	'jgwillgallerytemplate1910-dependency',
			//	FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'js/jgwillgallerytemplate1910-dependency.js',
			//	array(),
			//	FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_VERSION
			//);

			wp_enqueue_script(
				'jgwillgallerytemplate1910',
				FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'js/jgwillgallerytemplate1910.js',
				array(), //array('jgwillgallerytemplate1910-dependency'),
				FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_VERSION
			);

			foogallery_enqueue_style(
				'scattered-polaroids-gallery',
				FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'css/photostack.css',
				array(), //include any CSS dependencies here
				FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_VERSION
			);
		}

		/**
		 * Add our gallery template to the list of templates available for every gallery
		 * @param $gallery_templates
		 *
		 * @return array
		 */
		function add_template( $gallery_templates ) {

			$gallery_templates[] = array(
				'slug'            => 'jgwillgallerytemplate1910',
				'name'            => __( 'JGWIllGalleryTemplate1910', 'foogallery-jgwillgallerytemplate1910'),
				'preview_support' => true,
				'preview_css'     => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'css/gallery-jgwillgallerytemplate1910.css',
				'admin_js'	      => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'js/admin-gallery-jgwillgallerytemplate1910.js',
				'fields'	      => array(
					array(
						'id'      => 'thumbnail_dimensions',
						'title'   => __('Thumbnail Size', 'foogallery-jgwillgallerytemplate1910'),
						'desc'    => __('Choose the size of your thumbs.', 'foogallery-jgwillgallerytemplate1910'),
						'type'    => 'thumb_size',
						'default' => array(
							'width' => get_option( 'thumbnail_size_w' ),
							'height' => get_option( 'thumbnail_size_h' ),
							'crop' => true
						)
					),
					array(
						'id'      => 'thumbnail_link',
						'title'   => __('Thumbnail Link', 'foogallery-jgwillgallerytemplate1910'),
						'default' => 'image' ,
						'type'    => 'thumb_link',
						'spacer'  => '<span class="spacer"></span>',
						'desc'	  => __('You can choose to either link each thumbnail to the full size image or to the image\'s attachment page.', 'foogallery-jgwillgallerytemplate1910')
					),
					array(
						'id'      => 'lightbox',
						'title'   => __('Lightbox', 'foogallery-jgwillgallerytemplate1910'),
						'desc'    => __('Choose which lightbox you want to use in the gallery.', 'foogallery-jgwillgallerytemplate1910'),
						'type'    => 'lightbox'
					),
					array(
						'id'      => 'alignment',
						'title'   => __('Gallery Alignment', 'foogallery-jgwillgallerytemplate1910'),
						'desc'    => __('The horizontal alignment of the thumbnails inside the gallery.', 'foogallery-jgwillgallerytemplate1910'),
						'default' => 'alignment-center',
						'type'    => 'select',
						'choices' => array(
							'alignment-left' => __( 'Left', 'foogallery-jgwillgallerytemplate1910' ),
							'alignment-center' => __( 'Center', 'foogallery-jgwillgallerytemplate1910' ),
							'alignment-right' => __( 'Right', 'foogallery-jgwillgallerytemplate1910' )
						)
					)
					//available field types available : html, checkbox, select, radio, textarea, text, checkboxlist, icon
					//an example of a icon field used in the default gallery template
					//array(
					//	'id'      => 'border-style',
					//	'title'   => __('Border Style', 'foogallery-jgwillgallerytemplate1910'),
					//	'desc'    => __('The border style for each thumbnail in the gallery.', 'foogallery-jgwillgallerytemplate1910'),
					//	'type'    => 'icon',
					//	'default' => 'border-style-square-white',
					//	'choices' => array(
					//		'border-style-square-white' => array('label' => 'Square white border with shadow', 'img' => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'assets/border-style-icon-square-white.png'),
					//		'border-style-circle-white' => array('label' => 'Circular white border with shadow', 'img' => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'assets/border-style-icon-circle-white.png'),
					//		'border-style-square-black' => array('label' => 'Square Black', 'img' => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'assets/border-style-icon-square-black.png'),
					//		'border-style-circle-black' => array('label' => 'Circular Black', 'img' => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'assets/border-style-icon-circle-black.png'),
					//		'border-style-inset' => array('label' => 'Square Inset', 'img' => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'assets/border-style-icon-square-inset.png'),
					//		'border-style-rounded' => array('label' => 'Plain Rounded', 'img' => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'assets/border-style-icon-plain-rounded.png'),
					//		'' => array('label' => 'Plain', 'img' => FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE_URL . 'assets/border-style-icon-none.png'),
					//	)
					//),
				)
			);

			return $gallery_templates;
		}

		/**
		 * Build up the arguments needed for rendering the gallery template
		 *
		 * @param $args
		 * @return array
		 */
		function build_gallery_template_arguments( $args ) {
			$args = foogallery_gallery_template_setting( 'thumbnail_dimensions', array() );
			$args['crop'] = '1'; //we now force thumbs to be cropped
			$args['link'] = foogallery_gallery_template_setting( 'thumbnail_link', 'image' );

			return $args;
		}
	}
}

new FooGallery_JGWIllGalleryTemplate1910_Template();