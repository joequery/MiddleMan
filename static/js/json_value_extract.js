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
        var js_selector = "span[class^=hljs]"
        var $parents = $(e).parents(js_selector);

        var is_top_level_element = $parents.length == 0;
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
            log_el("not top level:", e);
            var $parent_vals = $(e).parents("span.hljs-value")
            if($parent_vals.length != 0){
                var selector = get_json_selector_type(e, $parent_vals);
                console.log("Selector type: " + selector.type);
                var $next = get_next_element($parent_vals, selector.type);
                return get_middleman_selector($next) + selector.selector;
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

    /*
     * Get the next element in the json traversal sequence based upon what kind
     * of selector we just found
     */
    var get_next_element = function(e, type){
        var $parents;
        if(type === "key"){
            $parents = traverse_to_closest(e, 'attribute');
        }
        return $parents;
    }

    var traverse_to_closest = function(e, kind){
        var selector = "span[class=hljs-" + kind + "]";
        var $prev = $(e).prev(selector);
        if ($prev.length != 0){
            return $prev;
        }
        else{
            var $parents = $(e).parents(selector);
            return $parents;
        }

    }


    var get_json_selector_type = function(e, $parents){
        var parent_html = $parents.html();
        var $siblings = $parents.children();
        var type, selector;
        if(parent_html[0] == "["){
            var index = $.inArray(e, $siblings);

            type = "element";
            selector = "[" + index + "]";
        }
        else if(parent_html[0] == "{"){
            var key = $siblings.html();

            type = "key";
            selector = "['" + key + "']";
        }
        return {selector: selector, type: type};
    };

});
