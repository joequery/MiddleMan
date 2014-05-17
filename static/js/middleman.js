// =========================================================
// Process middleman form
// =========================================================

$(function(){
    // ===================================================
    // Form processing
    // ===================================================
    window.$mm_form = $("#mm_form");
    window.$result_textarea = $("#results");
    window.$rawjson_textarea = $("#rawjson");
    // ===================================================
    // Sample data
    // ===================================================
    var $sampledata_btn = $("#get_example");
    $sampledata_btn.click(function(){
        $sampledata_btn.text("Now click submit below...");
        $sampledata_btn.attr("disabled", "disabled");
        $sampledata_btn.removeClass("btn-primary");

        var jqxhr = $.getJSON('/sampledata',
            function(resp, status) {
                url = resp.url;
                scheme = resp.scheme;
                $("#url").val(url);
                $("#scheme").text(scheme);
            }
        );
    });
});
