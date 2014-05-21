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
        //filter: 'code span:not(.hljs-attribute)'
        filter: 'code span'
    })
    DOutline.start()

    var log_el = function(msg, el){
        console.dirxml(msg, $(el));
    };

    var get_middleman_selector = function(e){
        $e = $(e);
        var js_selector = "span[class^=hljs]"
        var $parents = $e.parents(js_selector);

        var is_top_level_element = $parents.length == 0;
        if(is_top_level_element){
            // Top level is always a key
            var key = "['" + $e.text() + "']";

            // This ends the recursion
            return key;
        }
        else{
            // The first character of the parent lets us know what type of value
            // this is. We need to look for values first, then attributes if we
            // don't find any.
            var $parent_vals = $e.parents("span.hljs-value")
            log_el($e);
            if($parent_vals.length != 0){
                var selector = get_json_selector_type($e, $parent_vals);
                var $next = traverse_to_closest($parent_vals, 'attribute');
                console.log(selector);

                if(selector.selector){
                    return get_middleman_selector($next) + selector.selector;
                }
                else{
                    return get_middleman_selector($next);
                }
            }
        }
    };

    /*
     * Get the next element in the json traversal sequence based upon what kind
     * of selector we just found
     */
    /*
    var get_next_element = function(e, type){
        var $parents;
        if(type === "key"){
            $parents = traverse_to_closest(e, 'attribute');
        }
        else if(type === "element"){
            $parents = traverse_to_closest(e, 'attribute');
        }
        else if(type === "key-val"){
            $parents = traverse_to_closest(e, 'attribute');
        }
        return $parents;
    }
    */

    var traverse_to_closest = function(e, kind){
        var selector = "span[class=hljs-" + kind + "]";
        var $prev = $(e).prev(selector);
        if ($prev.length){
            return $prev.eq(0);
        }
        else{
            var $parents = $(e).parents(selector);
            if ($parents.length){
                return $parents.eq(0);
            }
            else{
                return false;
            }
        }

    }


    var get_json_selector_type = function(e, $parents){
        var parent_html = $parents.html();
        var $siblings = $parents.children();
        var type, selector;
        var first_char = parent_html[0];
        log_el('getting json type of', e);
        if(first_char == "["){
            var index = $.inArray(e, $siblings);

            type = "element";
            selector = "[" + index + "]";
        }
        else if(first_char == "{"){
            var key = e.text();

            type = "key";
            selector = "['" + key + "']";
        }
        else if (first_char == "<"){
            type = "key-val";
            selector = null;
        }
        else{
            console.log("UNRECOGNIZED");
            console.log(parent_html[0]);
        }
        return {selector: selector, type: type};
    };

});
