/*
 * jQuery attachInside plugin
 *
 * This plugin lets you stick some element "inside" other element
 * to become fixed during scrolling without overlapping other elements.
 *
 * Created by Andrew Dunai <andrew@dun.ai>
*/

$.fn.attachInside = function(opts) {
    var $el = $(this);

    var dataOpts;
    try {
        dataOpts = new Function('return ' + $el.attr('data-attach-inside'))();
    } catch(e) {
        dataOpts = null;
    }

    opts = opts || dataOpts || {};
    var overCover = opts.overCover || 0;
    var compensateMargin = opts.compensateMargin || true;
    var minScreenWidth = opts.minScreenWidth || 0;
    var maxScreenWidth = opts.maxScreenWidth || 0;
    var reserveSpace = opts.reserveSpace || true;
    var shift = opts.shift || 0;

    var $parent = opts.parent ? $(opts.parent) : $el.parent();
    var originalWidth = $el.get(0).getBoundingClientRect().width;
    var originalLeft = Math.floor($el.offset().left);
    var marginLeftCompensation = compensateMargin ? parseInt($el.css('margin-left')) : 0;

    var $dummy = null;
    if (reserveSpace) {
        $dummy = $('<' + $el.prop('tagName') + '/>');
        $dummy.addClass($el.prop('class'));

        $dummy.insertAfter($el);
    }

    var process = function () {
        var screenWidth = $(window).width();
        if (screenWidth <= minScreenWidth || (maxScreenWidth > 0 && screenWidth >= maxScreenWidth)) {
            $el.css('position', 'static');
            return;
        }

        var windowScrollAbs = $(window).scrollTop();

        var parentOffsetAbs = $parent.offset();
        var parentStartAbs = parentOffsetAbs.top;
        var parentEndAbs = parentOffsetAbs.top + $parent.height();

        var parentOffsetRel = {
            left: parentOffsetAbs.left,
            top: parentOffsetAbs.top - windowScrollAbs
        };

        if (windowScrollAbs > parentStartAbs - overCover) {
            // To top
            if ($dummy) {
                $dummy.css('display', '');
            }
            $el.css({
                position: 'fixed',
                left: originalLeft - marginLeftCompensation,
                top: shift,
                width: originalWidth
            });
            if (windowScrollAbs + $el.height() > parentEndAbs) {
                // To bottom
                $el.css({
                    top: parentEndAbs - (windowScrollAbs + $el.height())
                });
            }
        } else {
            if ($dummy) {
                $dummy.css('display', 'none');
            }
            $el.css('position', 'static');
            originalLeft = $el.offset().left;
        }
    };

    $(window).on('scroll resize', process);

    process();
};

$(window).ready(function() {
    $('[data-attach-inside]').each(function() {
        $(this).attachInside();
    });
});
