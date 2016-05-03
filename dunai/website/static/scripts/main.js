$(document).ready(function(){
    var bcTimeout = -1;

    var refresh = function() {
        $('.materialboxed').materialbox();
        $(".button-collapse").sideNav({closeOnClick: true, edge: 'right'});
        // $('.button-collapse').sideNav('hide');
    };

    // $('.button-collapse').on('click', function(e) {
    //     e.preventDefault();
    //     $(this).sideNav('show');
    // });

    var getState = function() {
        return {
            title: document.title.toString(),
            nav: $('#nav').first().html(),
            breadcrumbs: $('#breadcrumbs .container').first().html(),
            main: $('#main').first().html()
        };
    };

    // $('.slider').slider({full_width: true});

    window.onpopstate = function(e) {
        var stateObj = e.state;

        $('#loading-overlay').addClass('visible');

        document.title = stateObj.title;
        $('#nav').html(stateObj.nav);
        $('#breadcrumbs .container').addClass('invisible blurred');
        $('#main').addClass('invisible collapsed');
        if (bcTimeout >= 0) {
            window.clearTimeout(bcTimeout);
        }
        bcTimeout = window.setTimeout(function() {
            bcTimeout = -1;
            $('#breadcrumbs .container').html(stateObj.breadcrumbs);
            $('#main').html(stateObj.main);

            window.setTimeout(function() {
                $('#breadcrumbs .container').removeClass('invisible blurred');
                $('#main').removeClass('invisible collapsed');

                refresh();
            }, 10);

            $('#loading-overlay').removeClass('visible');
        }, 200);
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

        $.ajax({
            url: url,
            method: 'GET',
            timeout: 10000,
            success: function(data) {
                var $doc = $('<div/>');
                $doc.html(data);

                var title = $doc.find('title').first().html();
                var nav = $doc.find('#nav').first().html();
                var breadcrumbs = $doc.find('#breadcrumbs .container').first().html();
                var main = $doc.find('#main').first().html();

                history.pushState({
                    title: title,
                    nav: nav,
                    breadcrumbs: breadcrumbs,
                    main: main
                }, title, url);

                document.title = title;

                $('#nav').html(nav);
                $('#breadcrumbs .container').addClass('invisible blurred');
                $('#main').addClass('invisible collapsed');
                if (bcTimeout >= 0) {
                    window.clearTimeout(bcTimeout);
                }
                bcTimeout = window.setTimeout(function() {
                    bcTimeout = -1;
                    $('#breadcrumbs .container').html(breadcrumbs);
                    $('#main').html(main);

                    window.setTimeout(function() {
                        $('#breadcrumbs .container').removeClass('invisible blurred');
                        $('#main').removeClass('invisible collapsed');

                        refresh();
                    }, 10);

                    $('#loading-overlay').removeClass('visible');
                    // $link.removeClass('ps-loading');
                    busy = false;
                }, 200);

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
});
