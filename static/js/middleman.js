// =========================================================
// Process middleman form
// =========================================================

var scrollto_elem = function($jqobj){
    $('html, body').animate({scrollTop: $jqobj.offset().top -100 }, 'slow');
}

var process_json_scheme = function($form, $result_textarea){
    var data = $form.serialize();
    var jqxhr = $.post('/process',
        data,
        function(resp, status) {
            if (typeof(resp.errors) !== 'undefined'){
                $result_textarea.val(resp.errors.message);
            }
            else{
                scrollto_elem(window.$result_textarea);
                $result_textarea.val(resp.result);
            }
        }
    );
};

$(function(){
    // ===================================================
    // Form processing
    // ===================================================
    window.$mm_form = $("#mm_form");
    window.$result_textarea = $("#results");

    $mm_form.submit(function(e){
        process_json_scheme($(this), $result_textarea);
        e.preventDefault();
    });

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
                rawjson = resp.rawjson;
                scheme = resp.scheme;
                $("#rawjson").text(rawjson);
                $("#scheme").text(scheme);
            }
        );
    });
});
