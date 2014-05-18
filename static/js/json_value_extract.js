$(function(){
    var DomOutlineHandlers = {
        'click': function(e){
            console.log('Clicked element:', e);
        },
        'mouseover': function(e){
            $(".DomOutline").show();
            console.log('Hovered over element:', e);
        },
        'mouseout': function(e){
            $(".DomOutline").hide();
            console.log('Leaving element:', e);
        },
    }
    var DOutline = DomOutline({ handlers: DomOutlineHandlers, filter: 'code span' })
    /*
    var DOutline = DomOutline({
        filter: 'code span',
        onClick: function(e){
            console.log('Clicked element:', e);
        }
    })
    */
    DOutline.start()
});
