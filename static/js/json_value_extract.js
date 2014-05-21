$(function(){
    var DomOutlineHandlers = {
        'click': function(e){
            var sel = get_middleman_selector(e);
            console.log(sel);
        },
        'mouseover': function(e){
            $(".DomOutline").show();
        },
        'mouseout': function(e){
            $(".DomOutline").hide();
        },
    }
    var DOutline = DomOutline({
        handlers: DomOutlineHandlers,
        filter: 'code span:not(.hljs-attribute)'
    })
    DOutline.start()

    var get_middleman_selector = function(e){
        var is_top_level_element = $(e).parents("span[class^=hljs]").length == 0;
        if(is_top_level_element){
            // Top level is always a key
            var key = "['" + $(e).text() + "']";

            // This ends the recursion
            return key;
        }
        else{
            // The first character of the parent lets us know what type of value
            // this is. We need to look for values first, then attributes if we
            // don't find any.
            var $parent_vals = $(e).parents("span.hljs-value")
            if($parent_vals.length != 0){
                var selector = get_json_selector_type(e, $parent_vals);
                var $parent_vals = $parent_vals.parents("span.hljs-value").children('.hljs-attribute');
                return get_middleman_selector($parent_vals) + selector;
            }
            else{
                console.log("NO VALUES FOUND");
                var $parent_attrs = $(e).parentsUntil("span.hljs-attribute").parents();
                var $parent_text = $parent_attrs.html()

                if($parent_text[0] == "{"){
                    console.log("DO KEY!");
                }
            }
        }
    };

    var get_json_selector_type = function(e, $parents){
        var parent_html = $parents.html();
        var $siblings = $parents.children();
        if(parent_html[0] == "["){
            var index = $.inArray(e, $siblings);
            return "[" + index + "]";
        }
        else if(parent_html[0] == "{"){
            var key = $siblings.html();
            return "['" + key + "']";
        }
    };

});
