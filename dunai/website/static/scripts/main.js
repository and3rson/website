$(document).ready(function(){
    var bcTimeout = -1;

    var refresh = function() {
        $('.materialboxed').materialbox();
    };

    var getState = function() {
        return {
            title: document.title.toString(),
            nav: $('#nav').first().html(),
            breadcrumbs: $('#breadcrumbs .container').first().html(),
            main: $('#main').first().html()
        };
    };

    $('.slider').slider({full_width: true});
    $(".button-collapse").sideNav();

    window.onpopstate = function(e) {
        var stateObj = e.state;

        document.title = stateObj.title;
        $('#nav').html(stateObj.nav);
        $('#breadcrumbs .container').addClass('invisible blurred');
        $('#main').addClass('invisible collapsed');
        if (bcTimeout >= 0) {
            window.clearTimeout(bcTimeout);
        }
        bcTimeout = window.setTimeout(function() {
            bcTimeout = -1;
            $('#breadcrumbs .container').removeClass('invisible blurred');
            $('#breadcrumbs .container').html(stateObj.breadcrumbs);

            $('#main').removeClass('invisible collapsed');
            $('#main').html(stateObj.main);

            refresh();
        }, 200);
    };

    history.replaceState(getState(), document.title, document.location.toString());

    $(document).on('click', 'a[data-ps]', function(e) {
        var $link = $(this).first();

        e.preventDefault();

        var url = $link.attr('href');

        if(document.location.pathname == url) {
            // Do nothing.
            return;
        }

        $.ajax({
            url: url,
            method: 'GET',
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
                    $('#breadcrumbs .container').removeClass('invisible blurred');
                    $('#breadcrumbs .container').html(breadcrumbs);

                    $('#main').removeClass('invisible collapsed');
                    $('#main').html(main);

                    refresh();
                }, 200);

                $doc.remove();
            }
        });
    });
});
