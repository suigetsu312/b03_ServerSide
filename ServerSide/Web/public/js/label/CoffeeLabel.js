
// get references to the canvas and context
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

// style the context
ctx.strokeStyle = "blue";
ctx.lineWidth = 3;

// calculate where the canvas is on the window
// (used to help calculate mouseX/mouseY)
var $canvas = $("#canvas");
var canvasOffset = $canvas.offset();
var offsetX = canvasOffset.left;
var offsetY = canvasOffset.top;
if($(window).scrollTop() > 0){
    offsetY = canvasOffset.top-$(window).scrollTop();    
}
var scrollX = $canvas.scrollLeft();
var scrollY = $canvas.scrollTop();

$(window).resize(function(){
    canvasOffset = $canvas.offset();
    offsetX = canvasOffset.left;
    offsetY = canvasOffset.top;
    scrollX = $canvas.scrollLeft();
    scrollY = $canvas.scrollTop();

})

$(window).scroll(function(){
    var y = $(window).scrollTop()
    console.log(y)
    if (y>0){
        offsetY = canvasOffset.top-$(window).scrollTop();    
    }else{
        offsetY = canvasOffset.top;    
    }
    canvasOffset = $canvas.offset();
    offsetX = canvasOffset.left;
    scrollX = $canvas.scrollLeft();
    scrollY = $canvas.scrollTop();

})
// this flage is true when the user is dragging the mouse
var isDown = false;

// these vars will hold the starting mouse position
var startX;
var startY;
var height;
var width;
var RecordX;
var RecordY;
var RecordH;
var RecordW;

function handleMouseDown(e) {
    e.preventDefault();
    e.stopPropagation();

    // save the starting x/y of the rectangle
    startX = parseInt(e.clientX - offsetX);
    startY = parseInt(e.clientY - offsetY);
    // set a flag indicating the drag has begun
    isDown = true;
}

function handleMouseUp(e) {
    e.preventDefault();
    e.stopPropagation();

    // the drag is over, clear the dragging flag
    isDown = false;
}

function handleMouseOut(e) {
    e.preventDefault();
    e.stopPropagation();

    // the drag is over, clear the dragging flag
    isDown = false;
}

function handleMouseMove(e) {
    e.preventDefault();
    e.stopPropagation();

    // if we're not dragging, just return
    if (!isDown) {
        return;
    }

    // get the current mouse position
    mouseX = parseInt(e.clientX - offsetX);
    mouseY = parseInt(e.clientY - offsetY);

    // Put your mousemove stuff here

    // clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // calculate the rectangle width/height based
    // on starting vs current mouse position
    width = mouseX - startX;
    height = mouseY - startY;
    RecordH = height
    RecordW = width
    if (RecordX < 0 || RecordY <0){
        RecordY = mouseY
        RecordX = mouseX
    }
    else{
        RecordY = startY
        RecordX = startX
    }
    
    // draw a new rect from the start position 
    // to the current mouse position
    ctx.strokeRect(RecordX, RecordY, RecordW, RecordH);
    ctx.fillRect(RecordX,RecordY,1,1); 


}

// listen for mouse events
$("#canvas").mousedown(function (e) {
    handleMouseDown(e);
});
$("#canvas").mousemove(function (e) {
    handleMouseMove(e);
});
$("#canvas").mouseup(function (e) {
    handleMouseUp(e);
    var samples =  $('#samples');
    if(samples.children('tr').length != 0){
        var index = Number(samples.children('tr').last().children('td').first().text())+1
    }
    else{
        var index = 1;
    }

    var head = $('<td>').append($('<button>').attr('scope','row').text(index).attr('id','dis_bean').click(function(e){
        var canvas = document.getElementById("canvas");
        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        var h = Number($(this).parent().parent().children('#h_value').text())
        var w = Number($(this).parent().parent().children('#w_value').text())
        var x = Number($(this).parent().parent().children('#x_value').text())
        var y = Number($(this).parent().parent().children('#y_value').text())

        ctx.strokeRect(x+Math.floor(w/2), y+Math.floor(h/2), w, h);
    }))

    if( RecordH < 0 || RecordY <0){

    }
    var x = $('<td>').text(Math.abs(RecordX) + RecordW/2).attr('id','x_value')
    var y = $('<td>').text(Math.abs(RecordY) + RecordH/2).attr('id','y_value')
    var heightd = $('<td>').text(Math.abs(RecordH)).attr('id','h_value')
    var widthtd = $('<td>').text(Math.abs(RecordW)).attr('id','w_value')
    var selectClassStr = '<td><select class="form-control" id="BeanClass"><option value=0>normal</option><option value=1>broken</option><option value=2>insect</option></select></td>';				
    var selectClass = $(selectClassStr)
    
    var delbtn = $('<button>').attr('id','delSampleBtn').attr('class','btn btn-danger text-center').text('delete').attr('type','button').bind('click',function(e){
        if($(this).parent().parent().next().length){
            $(this).parent().parent().nextAll().each(function(){
                var number = Number($(this).children('td').first().children('button').text())-1
                $(this).children('td').first().children('button').text(number)
            })
            
        }
        $(this).parent().parent().remove()
    })
    var btntd = $('<td>').append(delbtn)
    var trow = $('<tr>').append(head).append(x).append(y).append(heightd).append(widthtd).append(selectClass).append(btntd)
    samples.append(trow)
});
$("#canvas").mouseout(function (e) {
    handleMouseOut(e);
});	