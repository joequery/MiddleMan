$(function(){
    var DomOutlineHandlers = {
        'click': function(e){
            log_el(e);
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
});
