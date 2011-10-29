(function ($) {
    $.extend({
        postJSON: function (url, json, success, options) {
            var config = {
                url: url,
                type: "POST",
                data: json ? JSON.stringify(json) : null,
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: success
            };
            $.ajax($.extend(options, config));
        }
    });
})(jQuery);