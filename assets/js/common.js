// aHR0cHM6Ly9naXRodWIuY29tL2x1b3N0MjYvYWNhZGVtaWMtaG9tZXBhZ2U=
$(function () {
    lazyLoadOptions = {
        scrollDirection: 'vertical',
        effect: 'fadeIn',
        effectTime: 300,
        placeholder: "",
        onError: function(element) {
            console.log('[lazyload] Error loading ' + element.data('src'));
        },
        afterLoad: function(element) {
            if (element.is('img')) {
                // remove background-image style
                element.css('background-image', 'none');
            } else if (element.is('div')) {
                // set the style to background-size: cover; 
                element.css('background-size', 'cover');
                element.css('background-position', 'center');
            }
        }
    }

    $('img.lazy, div.lazy:not(.always-load)').Lazy({visibleOnly: true, ...lazyLoadOptions});
    $('div.lazy.always-load').Lazy({visibleOnly: false, ...lazyLoadOptions});

    $('[data-toggle="tooltip"]').tooltip()

    // Collapse the mobile menu after picking a section.
    $('#navbarResponsive .nav-link').on('click', function () {
        $('#navbarResponsive').collapse('hide');
    });

    // Highlight the nav link of the section in view. Bootstrap's scrollspy only switches when a
    // section reaches the top of the viewport, which short pages on tall screens never do.
    var navLinks = Array.prototype.slice.call(document.querySelectorAll('#site-nav .nav-link[href^="#"]'));
    var navSections = navLinks.map(function (a) { return document.querySelector(a.getAttribute('href')); });
    var updateActiveLink = function () {
        if (!navLinks.length) return;
        var marker = window.innerHeight * 0.35;
        var current = 0;
        navSections.forEach(function (el, i) {
            if (el && el.getBoundingClientRect().top <= marker) current = i;
        });
        if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
            current = navLinks.length - 1;
        }
        navLinks.forEach(function (a, i) { a.classList.toggle('active', i === current); });
    };

    // Add a hairline under the navbar once the page is scrolled.
    var $nav = $('#site-nav');
    var onScroll = function () {
        $nav.toggleClass('is-scrolled', window.scrollY > 8);
        updateActiveLink();
    };
    $(window).on('scroll resize', onScroll);
    onScroll();
})
