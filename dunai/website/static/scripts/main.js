$(document).ready(function(){
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

        console.log('onPopState: title =', stateObj.title);

        document.title = stateObj.title;
        $('#nav').html(stateObj.nav);
        $('#breadcrumbs .container').addClass('invisible');
        window.setTimeout(function() {
            $('#breadcrumbs .container').removeClass('invisible');
            $('#breadcrumbs .container').html(stateObj.breadcrumbs);
        }, 250);
        $('#main').html(stateObj.main);
    };

    history.replaceState(getState(), document.title, document.location.toString());
    console.log('replaceState: title =', document.title);

    $(document).on('click', 'a:not([data-nops])', function(e) {
        var $link = $(this).first();

        e.preventDefault();

        var url = $link.attr('href');

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

                console.log('pushState: title =', title);

                document.title = title;

                $('#nav').html(nav);
                $('#breadcrumbs .container').addClass('invisible');
                window.setTimeout(function() {
                    $('#breadcrumbs .container').removeClass('invisible');
                    $('#breadcrumbs .container').html(breadcrumbs);
                }, 150);
                $('#main').html(main);

                $doc.remove();
            }
        });
    });
});
