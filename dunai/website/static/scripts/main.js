window.addEventListener('load', function(e) {
//    var $body = document.querySelector('body');
//    var $underlay = document.querySelector('.underlay');
//    Array.prototype.slice.call(document.querySelectorAll('[data-backgroundize]')).forEach(function(item) {
//        (function(element) {
//            element.addEventListener('mouseenter', function() {
//                var url = element.getAttribute('data-backgroundize');
//                $underlay.style.backgroundImage = 'url(' + url + ')';
//            });
//            element.addEventListener('mouseleave', function() {
//                console.log('leave');
//            });
//        })(item);
//    });

    //document.querySelectorAll('[]');

    var $lazyImages = document.querySelectorAll('img[data-src]');

    Array.prototype.slice.call($lazyImages).forEach(function($image) {
        var $offscreenImage = document.createElement('img');
        $offscreenImage.src = $image.getAttribute('data-src');
        $offscreenImage.addEventListener('load', function() {
            $image.src = $offscreenImage.src;
            window.setTimeout(function() {
                $image.setAttribute('class', $image.getAttribute('class') + ' loaded');
            }, 0);
        });
    });

    var $lazyDivs = document.querySelectorAll('div[data-src]');

    Array.prototype.slice.call($lazyDivs).forEach(function($div) {
        var $offscreenImage = document.createElement('img');
        $offscreenImage.src = $div.getAttribute('data-src');
        $offscreenImage.addEventListener('load', function() {
            $div.style.backgroundImage = 'url(' + $offscreenImage.src + ')';
            window.setTimeout(function() {
                $div.setAttribute('class', $div.getAttribute('class') + ' loaded');
            }, 0);
        });
    });

    var $openers = $('[data-nest]');

    var openNest = function($opener) {
        e && e.preventDefault();

        //history.pushState({open: $opener.attr('data-unique-id')}, window.title, $opener.attr('data-nest'));

        var $nest = $($('#nest-template').html());
        var $cover = $nest.find('.nest-cover');
        var $close = $nest.find('.nest-close');
        var $content = $nest.find('.nest-content');
        var bg = $opener.attr('data-nest-bg');

        var rect = $opener.get(0).getBoundingClientRect();
        $nest.css({
            position: 'fixed',
            left: rect.left,
            top: rect.top,
            width: rect.width,
            height: rect.height,
            zIndex: 100
        });

        $cover.css('background-image', 'url(' + bg + ')');

        var close = function () {
            //history.pushState({close: $opener.attr('data-unique-id')}, window.title, '/');

            $nest.removeClass('nest-maximized');

            window.setTimeout(function () {
                $nest.remove();
            }, 200);

            window.removeEventListener('keydown', escapeListener);
        };

        var escapeListener = function (e) {
            if (e.which == 27) {
                close();
            }
        };

        window.addEventListener('keydown', escapeListener);

        $close.on('click', close);

        $(document.body).append($nest);

        window.setTimeout(function () {
            $nest.addClass('nest-maximized');
        }, 25);

        window.setTimeout(function () {
            $.ajax({
                method: 'GET',
                url: $opener.attr('data-nest'),
                success: function (response) {
                    $content.html(response);
                },
                error: function (response) {
                    var $error = $($('#error-template').html());
                    $error.find('.code').html(response.status);
                    $error.find('.status').html(response.statusText + ' :-/');
                    $content.html($error);
                }
            });
        }, 200);
    };

    var lastId = 0;

    $openers.each(function() {
        var $opener = $(this);
        if (!$opener.attr('data-opener-id')) {
            $opener.attr('data-opener-id', ++lastId);
        }
        $opener.on('click', function (e) {
            e.preventDefault();
            openNest($opener);
        });
    //        //openNest($opener);
    });

    //var oldHash = '';
    //
    //var onHashChanged = function () {
    //    var current = window.location.hash.toString();
    //    if (oldHash != current) {
    //        var data = current.substr(1);
    //        if (!data.length) {
    //
    //        }
    //    //
    //    //    var args = data.split('/');
    //    //    if (args[0] == 'project') {
    //    //        console.log(args);
    //    //        var $opener = ('[data-opener-id="' + args[1] + '"]');
    //    //        openNest($opener);
    //    //    } else {
    //    //    }
    //    }
    //};
    //
    //$(window).on('hashchange', onHashChanged);
    //
    //onHashChanged();

    //window.onpopstate = function(state) {
    //    console.log(state);
    //};
});
