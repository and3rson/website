$(document).ready(function(){
    var bcTimeout = -1;

    var $bc = $('.breadcrumbs-ctn');
    var $bcInner = $bc.find('#breadcrumbs');
    var $parent = $bc.parent();

    var fixBreadcrumbs = function() {
        // console.log($bc.width(), $(window).width());
        // if ($parent.width() - $bc.width() < 80) {
            if ($(window).width() <= 992) {
                $bc.css({
                    width: Math.min($parent.width() - 40),
                });
            } else {
                $bc.css({
                    width: Math.min($parent.width() - $('#desktop-nav').width()),
                });
            }
            window.setTimeout(function() {
                $bcInner.scrollLeft(1000);
            }, 10);
        // }
    };

    $(".button-collapse").sideNav({closeOnClick: true, edge: 'right'});

    $('.dropdown-button').dropdown({
        inDuration: 100,
        outDuration: 250,
        constrain_width: false,
        hover: true,
        belowOrigin: true,
        alignment: 'right',
        stopPropagation: false
    });

    var refresh = function() {
        $('.materialboxed').materialbox();
        // $('.button-collapse').sideNav('hide');

        $('.dropdown-button').on('click', function(e) {
            e.preventDefault();
        }).on('mouseenter', function() {
        });

        fixBreadcrumbs();
        window.setTimeout(function() {
            fixBreadcrumbs();
        }, 100);
    };

    // $('.button-collapse').on('click', function(e) {
    //     e.preventDefault();
    //     $(this).sideNav('show');
    // });

    var getState = function() {
        return {
            title: document.title.toString(),
            nav: $('#nav').first().html(),
            breadcrumbs: $('#breadcrumbs').first().html(),
            main: $('#main').first().html()
        };
    };

    // $('.slider').slider({full_width: true});

    // var pathname = window.location.pathname.toString();

    window.onpopstate = function(e) {
        // console.log(window.location.pathname.toString(), pathname);
        // if (window.location.pathname.toString() == pathname) {
        //     console.log('STOP');
        //     return;
        // }
        // pathname = window.location.pathname.toString();
        var stateObj = e.state;

        if (!stateObj) {
            return;
        }

        $('#loading-overlay').addClass('visible');

        document.title = stateObj.title;
        // $('#nav').html(stateObj.nav);
        $('#nav [data-id]').removeClass('active').filter('[data-id="' + stateObj.navDataId + '"]').addClass('active');
        $('#breadcrumbs').addClass('invisible blurred collapsed');
        $('#main').addClass('invisible collapsed');
        if (bcTimeout >= 0) {
            window.clearTimeout(bcTimeout);
        }
        bcTimeout = window.setTimeout(function() {
            bcTimeout = -1;
            $('#breadcrumbs').html(stateObj.breadcrumbs);
            $('#main').html(stateObj.main);
            window.FB && FB.XFBML.parse();
            window.MathJax && window.MathJax.Hub && MathJax.Hub.Queue(["Typeset",MathJax.Hub,'main']);

            window.setTimeout(function() {
                $('#breadcrumbs').removeClass('invisible blurred collapsed');
                $('#main').removeClass('invisible collapsed');

                refresh();
            }, 10);

            $('#loading-overlay').removeClass('visible');
        }, 140);
    };

    history.replaceState(getState(), document.title, document.location.toString());

    var busy = false;

    $(document).off('.side-nav a')
    $(document).on('click', 'a[data-ps]', function(e) {
        var $link = $(this).first();

        e.preventDefault();

        var url = $link.attr('href');

        if(document.location.pathname == url) {
            // Do nothing.
            return;
        }

        if (busy) {
            return;
        }
        busy = true;
        $('#loading-overlay').addClass('visible');

        // $link.addClass('loading-colors');
        // return;

        $.ajax({
            url: url,
            method: 'GET',
            timeout: 10000,
            success: function(data) {
                var $doc = $('<div/>');
                $doc.html(data);

                var title = $doc.find('title').first().html();
                var navDataId = $doc.find('#nav [data-id].active').first().attr('data-id');
                var nav = $doc.find('#nav').first().html();
                var breadcrumbs = $doc.find('#breadcrumbs').first().html();
                var main = $doc.find('#main').first().html();

                history.pushState({
                    title: title,
                    navDataId: navDataId,
                    breadcrumbs: breadcrumbs,
                    main: main
                }, title, url);

                document.title = title;

                // $('#nav').html(nav);
                $('#nav [data-id]').removeClass('active').filter('[data-id="' + navDataId + '"]').addClass('active');
                $('#breadcrumbs').addClass('invisible blurred collapsed');
                $('#main').addClass('invisible collapsed');
                if (bcTimeout >= 0) {
                    window.clearTimeout(bcTimeout);
                }
                bcTimeout = window.setTimeout(function() {
                    bcTimeout = -1;
                    $('#breadcrumbs').html(breadcrumbs);
                    $('#main').html(main);
                    $(window).scrollTop(0);
                    window.FB && FB.XFBML.parse(); 
                    window.MathJax && window.MathJax.Hub && MathJax.Hub.Queue(["Typeset",MathJax.Hub,'main']);

                    $('#breadcrumbs').removeClass('invisible blurred collapsed');
                    $('#main').removeClass('invisible collapsed');

                    window.setTimeout(function() {
                        refresh();
                    }, 10);

                    $('#loading-overlay').removeClass('visible');
                    // $link.removeClass('ps-loading');
                    busy = false;
                }, 140);

                $doc.remove();
            },
            error: function() {
                busy = false;
                $('#loading-overlay').removeClass('visible');
                Materialize.toast('<i class="material-icons" style="margin-right: 1rem; font-size: 3rem">warning</i>Oops! Failed to load page!<br />Is your internet connection fine?', 5000);
            }
        });
    });

    refresh();
    $(window).on('resize', fixBreadcrumbs);

    $('[data-show-things]').on('click', function(e) {
        e.preventDefault();
        var $link = $(this);
        var toShow = $link.attr('data-show-things');
        var $toShow = $('#' + toShow);
        var $toHide = $('#' + ((toShow == 'good') ? 'bad' : 'good'));

        $toHide.addClass('minimized');
        window.setTimeout(function() {
            $toShow.removeClass('minimized');
        }, 200);
    });
});
