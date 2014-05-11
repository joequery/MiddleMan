// =========================================================
// Process middleman form
// =========================================================
var process_json_scheme = function($form, $result_textarea){
    var data = $form.serialize();
    var jqxhr = $.post('/process',
        data,
        function(resp, status) {
            console.log(resp);
            if (typeof(resp.errors) !== 'undefined'){
                $result_textarea.val(resp.errors.message);
            }
            else{
                $result_textarea.val(resp.result);
            }
        }
    );
};

$(function(){
    var $mm_form = $("#mm_form");
    var $result_textarea = $("#results");

    $mm_form.submit(function(e){
        process_json_scheme($(this), $result_textarea);
        e.preventDefault();
    });
});
