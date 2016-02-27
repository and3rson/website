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

    var $nests = document.querySelectorAll('[data-nest]');

    Array.prototype.slice.call($nests).forEach(function($nest) {
        $nest.addEventListener('click', function(e) {
            e.preventDefault();

            var bg = $nest.getAttribute('data-nest-bg');
            var $inside = document.createElement('div');
            $inside.setAttribute('class', 'nest');

            var rect = $nest.getBoundingClientRect();
            $inside.style.position = 'fixed';
            $inside.style.left = rect.left + 'px';
            $inside.style.top = rect.top + 'px';
            $inside.style.width = rect.width + 'px';
            $inside.style.height = rect.height + 'px';
            $inside.style.zIndex = 100;

            var $bg = document.createElement('div');
            $bg.setAttribute('class', 'nest-cover');
            $bg.style.backgroundImage = 'url(' + bg + ')';
            $inside.appendChild($bg);

            var $close = document.createElement('div');
            $close.setAttribute('class', 'nest-close');
            $inside.appendChild($close);

            var $content = document.createElement('div');
            $content.setAttribute('class', 'nest-content');
            $inside.appendChild($content);

            var close = function() {
                $inside.setAttribute('class', $inside.getAttribute('class').replace(/nest-maximized/, '').trim());

                window.setTimeout(function () {
                    $inside.parentNode.removeChild($inside);
                }, 200);

                window.removeEventListener('keydown', escapeListener);
            };

            var escapeListener = function(e) {
                console.log('CLOSE');
                if (e.which == 27) {
                    close();
                }
            };

            window.addEventListener('keydown', escapeListener);

            $close.addEventListener('click', close);

            document.body.appendChild($inside);

            window.setTimeout(function() {
                $inside.setAttribute('class', $inside.getAttribute('class') + ' nest-maximized');
            }, 25);

            window.setTimeout(function() {
                $.ajax({
                    method: 'GET',
                    url: $nest.getAttribute('data-nest'),
                    success: function (response) {
                        $($content).html(response);
                    }
                });
            }, 200);
        });
    });
});
