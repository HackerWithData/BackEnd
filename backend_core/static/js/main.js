jQuery(document).ready(function ($) {

    'use strict';

    $('.logoutButton').click(function (event) {
            $(this).parent('form').submit();
        }
    );

    $(".dashboard-content .alert").fadeTo(2000, 500).slideUp(500, function () {
        $(".dashboard-content .alert").slideUp(500);
    });

    // $(".alert-base.alert").fadeTo(2000, 500).slideUp(500, function () {
    //     $(".alert-base.alert").slideUp(500);
    // });

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


    $(".b1").click(function () {
        $(".pop").fadeIn(300);

    });

    $(".b2").click(function () {
        $(".pop2").fadeIn(300);

    });

    $(".b3").click(function () {
        $(".pop3").fadeIn(300);

    });

    $(".pop > span, .pop").click(function () {
        $(".pop").fadeOut(300);
    });

    $(".pop2 > span, .pop2").click(function () {
        $(".pop2").fadeOut(300);
    });

    $(".pop3 > span, .pop3").click(function () {
        $(".pop3").fadeOut(300);
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