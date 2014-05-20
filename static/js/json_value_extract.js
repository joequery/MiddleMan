$(function(){
    var DomOutlineHandlers = {
        'click': function(e){
            console.log("You clicked: ", e);
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

});
