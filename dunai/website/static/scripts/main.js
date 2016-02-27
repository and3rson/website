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

    $openers.each(function() {
        var $opener = $(this);
        $opener.on('click', function(e) {
            e.preventDefault();

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

            var close = function() {
                $nest.removeClass('nest-maximized');

                window.setTimeout(function () {
                    $nest.remove();
                }, 200);

                window.removeEventListener('keydown', escapeListener);
            };

            var escapeListener = function(e) {
                if (e.which == 27) {
                    close();
                }
            };

            window.addEventListener('keydown', escapeListener);

            $close.on('click', close);

            $(document.body).append($nest);

            window.setTimeout(function() {
                $nest.addClass('nest-maximized');
            }, 25);

            window.setTimeout(function() {
                $.ajax({
                    method: 'GET',
                    url: $opener.attr('data-nest'),
                    success: function (response) {
                        $content.html(response);
                    },
                    error: function(response) {
                        var $error = $($('#error-template').html());
                        $error.find('.code').html(response.status);
                        $error.find('.status').html(response.statusText + ' :-/');
                        $content.html($error);
                    }
                });
            }, 200);
        });
    });
});
