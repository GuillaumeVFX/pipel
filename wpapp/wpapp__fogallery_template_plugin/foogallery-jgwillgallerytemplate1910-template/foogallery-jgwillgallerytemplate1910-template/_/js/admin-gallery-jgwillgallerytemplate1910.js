//Use this file to inject custom javascript behaviour into the foogallery edit page
//For an example usage, check out wp-content/foogallery/extensions/default-templates/js/admin-gallery-default.js

(function (FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE, $, undefined) {

	FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE.doSomething = function() {
		//do something when the gallery template is changed to jgwillgallerytemplate1910
	};

	FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE.adminReady = function () {
		$('body').on('foogallery-gallery-template-changed-jgwillgallerytemplate1910', function() {
			FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE.doSomething();
		});
	};

}(window.FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE = window.FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE || {}, jQuery));

jQuery(function () {
	FOOGALLERY_JGWILLGALLERYTEMPLATE1910_TEMPLATE.adminReady();
});