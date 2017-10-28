jQuery(document).ready(function ($) {

    'use strict';

    $('.logoutButton').click(function (event) {
            $(this).parent('form').submit();
        }
    );

    $(".dashboard-content .alert").fadeTo(2000, 500).slideUp(500, function () {
        $(".dashboard-content .alert").slideUp(500);
    });


    $('#primary-menu').click(function () {
        if ($('.mobile-dropdown-group').hasClass('hide')) {
            $('.mobile-dropdown-group').removeClass('hide');
            $('#main-nav ul.nav.navbar-nav').css('height', ($('#main-nav ul.nav.navbar-nav').height() + 120));
        } else {
            $('.mobile-dropdown-group').addClass('hide');
            $('#main-nav ul.nav.navbar-nav').css('height', ($('#main-nav ul.nav.navbar-nav').height() - 120));
        }
    });


    $('.counter').each(function () {
        var $this = $(this),
            countTo = $this.attr('data-count');

        $({countNum: $this.text()}).animate({
                countNum: countTo
            },

            {

                duration: 8000,
                easing: 'linear',
                step: function () {
                    $this.text(Math.floor(this.countNum));
                },
                complete: function () {
                    $this.text(this.countNum);
                    //alert('finished');
                }

            });

    });


    $(window).on("scroll", function () {
        if ($(window).scrollTop() > 100) {
            $(".header").addClass("active");
        } else {
            //remove the background property so it comes transparent again (defined in your css)
            $(".header").removeClass("active");
        }
    });


    /************** Mixitup (Filter Projects) *********************/
    $('.projects-holder').mixitup({
        effects: ['fade', 'grayscale'],
        easing: 'snap',
        transitionSpeed: 400
    });


});

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return decodeURI(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function searchTargetTypeSuccess(data, textStatus, jqXHR) {
    $('#contractor-search-results').html(data)
}
