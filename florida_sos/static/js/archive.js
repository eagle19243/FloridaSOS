window.onload = function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);

                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }

    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         }
    });

    $("#btn_archive").click(function() {
        var google_sheet_url = $("#google_sheet_url").val();

        if (google_sheet_url.trim() === "") {
            $('.progress-status').html('Please enter a Google Spreadsheet URL');
            return;
        }

        $(".progress").asProgress("go", "0%");
        $(".progress").show();
        $('.progress-status').html('Processing...');
        var retry_failed_archives = ($("#retry_failed_archives:checked").length > 0);

        $.ajax({
            url: location.pathname,
            method: "POST",
            data: {
                    "google_sheet_url" : google_sheet_url,
                    "retry_failed_archives" : retry_failed_archives
            },
            success: function(res){
                if (res.success) {
                    var timer = setInterval(function(){
                        $.ajax({
                            url: location.pathname + "/get_progress",
                            method: "GET",
                            data: {job: res.job},
                            success: function(res) {
                                res = JSON.parse(res);

                                if (res.current === undefined) return;

                                if (res.error.length > 0) {
                                    $('.progress-status').html(res.error);
                                    $(".progress").asProgress("go", "0%");
                                    clearInterval(timer);
                                    return;
                                }

                                if (res.current == res.total) {
                                    $(".progress").asProgress("go", res.percent + "%");
                                    $('.progress-status').html(
                                            'Done! ' +
                                            res.total + ' of ' + res.total +
                                            ' processed with ' + res.fails + ' errors'
                                        );
                                    $('.progress-url').html("");
                                    clearInterval(timer);
                                } else {
                                    $(".progress").asProgress("go", res.percent + "%");
                                    $('.progress-status').html('Processed ' + res.current + ' of ' + res.total +
                                        ' with ' + res.fails + ' errors');
                                    $('.progress-url').html(res.url);
                                }
                            }
                        });
                    }, 1000);
                } else {
                    $('.status').html('Failed: ' + res.message);
                }
            }
        });
    });
}
