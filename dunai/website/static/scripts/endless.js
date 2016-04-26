$(function($) {
    $.fn.endless = function(opts) {
        var $el = $(this);

        var dataOpts;
        try {
            dataOpts = new Function('return ' + $el.attr('data-endless'))();
        } catch (e) {
            dataOpts = null;
        }

        opts = opts || dataOpts || {};

        $(window).on('scroll', function() {
            // console.log('Scroll');
        });
    };

    $(window).ready(function() {
        $('[data-endless]').each(function () {
            $(this).endless();
        });
    });
});
