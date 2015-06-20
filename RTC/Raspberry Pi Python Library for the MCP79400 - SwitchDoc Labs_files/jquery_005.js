jQuery(document).ready(function() {
	
	// Clear Widgets
	var counterWidget = 0;
	var limit = 4;
	
	if(jQuery('#footer').length){
	if (jQuery('#footer').hasClass('four-column-footer')) {
		limit = 4;
	} else if (jQuery('#footer').hasClass('three-column-footer')) {
		limit = 3;
	} else if (jQuery('#footer').hasClass('two-column-footer')) {
		limit = 2;
	} else if (jQuery('#footer').hasClass('one-column-footer')) {
		limit = 1;
	}
	}
	
	if(jQuery('#footer').length){
	jQuery('#footer .widget-column').each(function () {
		var currentItem = jQuery(this);
		counterWidget++;

		var number = parseInt(counterWidget);
		if(number == limit) { jQuery(this).addClass('last-column'); counterWidget = 0; }
	});
	}
	
	// Initialize menu
	if (jQuery('#nav').length){
		/*jQuery('#nav').supersubs({ 
            minWidth:    16,   // minimum width of sub-menus in em units 
            maxWidth:    30,   // maximum width of sub-menus in em units 
            extraWidth:  1.5     // extra width can ensure lines don't sometimes turn over 
                               // due to slight rounding differences and font-family 
        }).superfish({hoverClass:'sfHover', pathClass:'sf-active', pathLevels:0, delay:200, animation:{opacity:'show', height:'show'}, speed:'fast', autoArrows:1, dropShadows:0});*/
		jQuery('#nav').superfish({hoverClass:'sfHover', pathClass:'sf-active', pathLevels:0, delay:500, animation:{opacity:'show', height:'show'}, speed:'fast', autoArrows:1, dropShadows:0});


		if ( jQuery('.megamenu').length ){
			jQuery('.megamenu').each(function() {
				var element = jQuery(this);
				var first_ul = element.find(">ul").css("display", "block");

				var $mega_lis = first_ul.find('>li');
				var max = Math.max.apply(Math, $mega_lis.map(function() { return jQuery(this).height(); }));
				$mega_lis.css("height", max);
				first_ul.css("display", "none");
			});
		}


		
		// Navigation Icons
		jQuery("#nav li a").each(function() {
			jQuery(this).prepend('<span></span>')
		});	
		
		// Remove all classes except one
		(function($) {
			$.fn.excludeClass = function($class) {
				var that = this;
				var element = that[0];
				var cls = element.className;
				var parts = cls.split(' ');
		
				for (var i = 0; i < parts.length; i++) {
					var part = parts[i];
					if (part != $class) {
						element.className = element.className.replace(part, '');
					}
				}
				return that;
			}
		})(jQuery);
		
		// Populate dropdown with menu items
		jQuery("#nav").each(function() {
			var elementmenu = jQuery(this).html();
			jQuery('ul#nav-resp').append('<li>' + elementmenu + '</li>');
			
			var className;
			jQuery('ul#nav-resp *').each(function() {
				className = "";
				var element = jQuery(this);
				if( jQuery(this).attr('class') != 'triangle') {
					if( jQuery(this).attr('class') != null) {
						
						var getClassName = [];
						getClassName = jQuery(element).attr('class').split(" ");
						
						for(var i = 0; i < getClassName.length; i++) {
							if (getClassName[i].substring(0,5) == 'icon-'){
								className = getClassName[i];
							}
							if (getClassName[i] == 'sf-sub-indicator'){
								className = getClassName[i];
							}
						}	
					}
					
						if ( className.substring(0,5) == 'icon-' ){
						jQuery(element).removeClass();
						jQuery(element).addClass(className);
					} else if (className == 'sf-sub-indicator'){
						jQuery(element).removeClass();
						jQuery(element).addClass(className);
					}
					 else {
						jQuery(element).removeClass();
					}
				}
			});
		
			jQuery('ul#nav-resp ul, ul#nav-resp li, ul#nav-resp a').removeAttr('style');
		});

		// RESPONSIVE MENU
		
		/* toggle nav */
		jQuery("#menu-icon").on("click", function(e){
			e.stopPropagation(); // This is the preferred method.   
			jQuery("#nav-resp").fadeToggle(150);
			jQuery(this).toggleClass("active");
			jQuery('#main-content, #footer, #bottom-line, #logo-wrap, #slider-section, #social-wrap').toggleClass('inactive-opacity');
			return false;
		});
		
		jQuery("#nav-resp").click(function(e) {
			e.stopPropagation(); // This is the preferred method.
			//return false;  
		});
		
		jQuery(document).click(function () {
			if (jQuery("#nav-resp").is(":visible") ) {
				jQuery('#nav-resp').fadeToggle(150);
				jQuery('#menu-icon').toggleClass("active");
				jQuery('#main-content, #footer, #bottom-line, #logo-wrap, #slider-section, #social-wrap').toggleClass('inactive-opacity');
				return false;
			}
			
		});
	}

	if( jQuery('.new-marker').length) {
		jQuery('.new-marker > a').append('<span class="new-marker-unit">NEW</span>');
	}
	
	/* Progress Bar */
	jQuery('.progress-bar .progress').each(function(){
		$progress = jQuery(this).attr('data-progress');
		jQuery(this).find('span').animate({ width : $progress+'%', 'opacity' : 1}, 500);
	});
	
	/* Header Dropdown */
	var headerFlag = false;
	jQuery('#header-dropdown .arrow-down').live('click', function() {
		var parent = jQuery(this).parent();
		var height = 380;
		
		if (headerFlag == false) {
			jQuery(parent).stop(true,false).animate({'margin-top':0},{
                    duration: 500,
                    easing: 'easeOutQuad'
            });
			headerFlag = true;
		}
		
		else {
			jQuery(parent).stop(true,false).animate({'margin-top':-height},{
                    duration: 500,
                    easing: 'easeOutQuad'
            });
			headerFlag = false;	
		}
		
	});
	
	
	jQuery('#close-map-info').click(function() {
		jQuery('#map-contact-info').hide(300);
	});
	
	
	if (jQuery('.fitVids').length) {
		jQuery('.fitVids').fitVids();
	}
	
	
/*-----------------------------------------------------------------------------------*/
/*	POSTS GRID
/*-----------------------------------------------------------------------------------*/ 
jQuery(document).ready(function($){
 var $container = jQuery('.posts-grid');
	$container.imagesLoaded( function(){
		$container.isotope({
			itemSelector : '.post',
			animationEngine : 'jquery'
		});	
	});
	
	jQuery(window).resize(function() {
			$container.isotope('reLayout');
		});
});
	
	
	// Isotope Portfolio filtering and animation
	if (jQuery("#portfolio-container-sec").length)
	{
		var $container = jQuery('#portfolio-container-sec');

		$container.isotope(
		{
			itemSelector: '.from-the-portfolio-sec',
			animationEngine : 'jquery'
		});

		var $optionSets = jQuery('#sort-categories'),
			$optionLinks = $optionSets.find('a');

		jQuery(window).resize(function() {
			$container.isotope('reLayout');
		});	

		$optionLinks.click(function ()
		{
			var $this = jQuery(this);
			// don't proceed if already selected
			if ($this.hasClass('current-category'))
			{
				return false;
			}
			var $optionSet = $this.parents('#sort-categories');
			$optionSet.find('li').removeClass('current-category');
			$this.parent().addClass('current-category');

			// make option object dynamically, i.e. { filter: '.my-filter-class' }
			var options = {},
				key = $optionSet.attr('data-option-key'),
				value = $this.attr('data-option-value');
			// parse 'false' as false boolean
			value = value === 'false' ? false : value;
			options[key] = value;
			if (key === 'layoutMode' && typeof changeLayoutMode === 'function')
			{
				// changes in layout modes need extra logic
				changeLayoutMode($this, options);
			}
			else
			{
				// otherwise, apply new options
				$container.isotope(options);
			}

			return false;
		});
	}
	
	
	// Isotope Portfolio filtering and animation
	if (jQuery("#portfolio-container-gal").length)
	{
		var $container = jQuery('#portfolio-container-gal');

		$container.isotope(
		{
			itemSelector: '.from-the-portfolio-gal',
			animationEngine : 'jquery'
		});

		var $optionSets = jQuery('#sort-categories'),
			$optionLinks = $optionSets.find('a');

		jQuery(window).resize(function() {
			$container.isotope('reLayout');
		});	

		$optionLinks.click(function ()
		{
			var $this = jQuery(this);
			// don't proceed if already selected
			if ($this.hasClass('current-category'))
			{
				return false;
			}
			var $optionSet = $this.parents('#sort-categories');
			$optionSet.find('li').removeClass('current-category');
			$this.parent().addClass('current-category');

			// make option object dynamically, i.e. { filter: '.my-filter-class' }
			var options = {},
				key = $optionSet.attr('data-option-key'),
				value = $this.attr('data-option-value');
			// parse 'false' as false boolean
			value = value === 'false' ? false : value;
			options[key] = value;
			if (key === 'layoutMode' && typeof changeLayoutMode === 'function')
			{
				// changes in layout modes need extra logic
				changeLayoutMode($this, options);
			}
			else
			{
				// otherwise, apply new options
				$container.isotope(options);
			}

			return false;
		});
	}
	
	
	/* Separators Fixes */
	jQuery(window).resize(function () {
		if ( jQuery('.separator-text').length ) {
		jQuery('.separator-text').each(function () {
					
			var cssWidth = jQuery(this).width();
			jQuery(this).css('left', ( jQuery(this).parent().width() - cssWidth - 40)/2  );
			
		})
		}
		

	});
	if ( jQuery('.separator-text').length ) {
	jQuery('.separator-text').each(function () {
				
		var cssWidth = jQuery(this).width();
		jQuery(this).css('left', ( jQuery(this).parent().width() - cssWidth - 40)/2  );
	
	})
	}
	
	
	if (jQuery(".from-the-portfolio-sec, .post-featured-image").length)
	{
		jQuery('.from-the-portfolio-sec, .post-featured-image').find('img').hover( function () {
			jQuery(this).stop(true, false).animate(
			{opacity: 0.3}, 150, 'easeInOutQuad');
		}, function () {
				jQuery(this).stop(false, true).animate({opacity: 1}, 300, 'easeInOutQuad');
		});
	}
	
	if (jQuery(".from-the-portfolio-gal").length)
	{
		jQuery('.from-the-portfolio-gal').hover( function () {
			jQuery(this).find('.overlay-info').stop(false, true).animate(
			{opacity: 0.9}, 150, 'easeInOutQuad');
		}, function () {
			jQuery(this).find('.overlay-info').stop(false, true).animate(
			{opacity: 0}, 150, 'easeInOutQuad');
		});
	}
	
	
	// Clear Inputs
	jQuery('input[type=text],textarea, input[type=password], input[type=email], input[type=search]').focus(
		function () {
			if (this.value == this.defaultValue) {
			this.value = '';
		}
	});
	
	
	/* Tab boxes */
	if (jQuery(".tabs_container").length){
	jQuery(".tabs_container .tab_content").hide();
	jQuery(".tabs_container ul.tabs").find("li:first").addClass("active").show();
	jQuery(".tabs_container").find(".tab_content:first").show();

	jQuery("ul.tabs li").click(function() {
		var tabs_container = jQuery(this).parent().parent();
		var tabs = tabs_container.children(".tabs");
		var tabs_contents = tabs_container.children(".tabs_contents");
		
		tabs.children("li").removeClass("active");
		jQuery(this).addClass("active");
		
		var clicked_li_id = tabs.children("li").index(this);
		var tab_content = tabs_contents.children("div").eq(clicked_li_id);
		
		tabs_contents.children(".tab_content").hide();
		jQuery(tab_content).fadeIn(400);
		return false;
	});
	}
	
	// Toggle
	if(jQuery(".toggle-unit").length) {
		jQuery(".toggle-container-wrapper").hide();
		 
		jQuery(".trigger").toggle(function(){
			jQuery(this).addClass("active");
			}, function () {
			jQuery(this).removeClass("active");
		});
		jQuery(".trigger").click(function(){
			jQuery(this).next(".toggle-container-wrapper").slideToggle();
		});
		

	}
	
	
	
	
	// Accordion
	if(jQuery(".accordion-unit").length){
	jQuery('.accordion').hide();
		
	jQuery('.trigger-button').click(function() {
		jQuery(".trigger-button").removeClass("active")
	 	jQuery('.accordion').slideUp('normal');
		if(jQuery(this).next().is(':hidden') == true) {
			jQuery(this).next().slideDown('normal');
			jQuery(this).addClass("active");
		 } 
	 });
	
	}
	
	
	// Gallery image hover
	jQuery('.gallery-item').hover(function () { 
		
		jQuery(this).find('p').stop(true,false).animate(
			{bottom: 5, opacity:1}, 250, 'easeInOutQuad' );
		}, function () {
		jQuery(this).find('p').stop(true,false).animate(
			{bottom: -50, opacity:0}, 350, 'easeInOutQuad');
			
	});
	
	if(jQuery().fancybox) {
			jQuery("a.fancybox").fancybox({
				'transitionIn'	:	'fade',
				'transitionOut'	:	'fade',
				'speedIn'		:	300, 
				'speedOut'		:	300, 
				'overlayShow'	:	true,
				'autoScale'		:	true,
				'titleShow'		: 	false,
				'margin'		: 	10
			});
			
			jQuery("a.fancy-iframe").fancybox({
				'type'			: 'iframe'
			});
	}
	
	
	// Tipsy Effect
	
	jQuery('#sort-categories li a, .blog-post-meta a').tipsy(
	{
		gravity: 's',
		opacity: 1,
		offset: 7,
		fade: true
		
	});
	
	jQuery('.tooltip').tipsy(
	{
		gravity: 's',
		opacity: 1,
		offset: 1,
		fade: true
		
	});
	
	jQuery('.separator-icon, .separator-top, .tagcloud a').tipsy(
	{
		gravity: 's',
		opacity: 1,
		offset: -5,
		fade: true
		
	})
	
	jQuery('.flexslider').hover(function () {
		jQuery(this).find('.flex-prev').stop(false, false).animate({left: 0}, 300, 'easeInOutQuad');
		jQuery(this).find('.flex-next').stop(false, false).animate({right: 0}, 300, 'easeInOutQuad');
	}, 
		function () {
			jQuery(this).find('.flex-prev').stop(false, false).animate({left: -35}, 300, 'easeInOutQuad');
			jQuery(this).find('.flex-next').stop(false, false).animate({right: -35}, 300, 'easeInOutQuad');
	})
	
	// Info Box click function 
		
		jQuery('.close-info-box').click(function (e) {
			
			e.preventDefault();
			
			jQuery(this).parent().animate( {opacity:0}, 200, function () {
				jQuery(this).animate( {opacity:0}, 50, function () {
					jQuery(this).parent().animate( {opacity:0}, 150, function () { jQuery(this).hide(); });
				});
			});
		});
		
		
	/* Scroll to top -------------------------------------------------*/
	/* Scroll To Top
        --------------------------------------------------------------------- */
		if ( jQuery('body').is('.login') ) return false;
		if ( !(jQuery('body').is('.kikkey-top')) ) return false;
		else {
			
		 	// Build Scroll To Top
            jQuery("<a href='#' id='scrollTop'><span class='icon-angle-up'></span></a>").appendTo("body");
			
            var showHeight = jQuery(window).height()/2 + 250;
			var scrollTop = jQuery('#scrollTop');

            // Check on page load
            if(jQuery(window).scrollTop() > (showHeight)) {
                jQuery('#scrollTop').show();
            }

            // Check on scroll event
            jQuery(window).scroll(function () {
                if(jQuery(window).scrollTop() > (showHeight)) {
                    jQuery('#scrollTop').show();
                } else {
                    jQuery('#scrollTop').hide();
                }
            });
			
		}
	
	
    jQuery('#scrollTop, .separator-top').click(function(e) {
		e.preventDefault();
		jQuery('body,html').animate({ scrollTop: "0" });
	});
	
	// Blog rate system.
		function bt_reloadLikes(who)
		{

			var text = jQuery("#" + who).html();
			var patt = /(\d)+/;
			var num = patt.exec(text);
			num[0]++;

			text = text.replace(patt, num[0]);

			jQuery("#" + who).html(text);

		} //reloadLikes
		function bt_likeInit()
		{
			jQuery(".like-button").click(function ()
			{
				var classes = jQuery(this).attr("class");
				classes = classes.split(" ");

				if (classes[1] == "like-active")
				{
					return false;
				}

				var classes = jQuery(this).addClass("like-active");
				var id = jQuery(this).attr("id");
				id = id.split("like-");

				jQuery.ajax(
				{
					type: "POST",
					url: "index.php",
					data: "likepost=" + id[1],
					success: bt_reloadLikes("like-" + id[1])
				});

				return false;
			});

			jQuery("a.like-count-sec").click(function ()
			{
				var classes = jQuery(this).attr("class");
				classes = classes.split(" ");

				if (classes[1] == "like-active")
				{
					return false;
				}

				var classes = jQuery(this).addClass("like-active");
				var id = jQuery(this).attr("id");
				id = id.split("like-");

				jQuery.ajax(
				{
					type: "POST",
					url: "index.php",
					data: "likepost=" + id[1],
					success: bt_reloadLikes("like-" + id[1])
				});

				return false;
			});
		}

		bt_likeInit();
		

		// Sticky Navigation
		if ( jQuery('#header').hasClass('hb_sticky_nav') ){
			jQuery('#main-navigation-wrapper').sticky();
		}
});