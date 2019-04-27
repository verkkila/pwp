'use strict';

function setRows(body){
    let items = body.items;
    items.forEach(function(item) {
        updateRow(item)
    });
    let tableRows = ($('tbody tr td[contentEditable=true]'));
    tableRows.on("blur", function(){
        let outData = {}
        outData.name = $(this).parent().children('.name').html().trim()
        outData.start_time = $(this).parent().children('.start_time').html().trim()
        outData.end_time = $(this).parent().children('.end_time').html().trim()
        let url = "http://localhost:5000/diary/schedules/" + $(this).parent().children('.id').html().trim() + '/';
        $.ajax({
            url:url,
            method:"PUT",
            data:JSON.stringify(outData),
            contentType: MASON,
            success: null
        });
    });
}

function updateRow(item){
    let tbody = $(".resulttable tbody");
    let htmlStr = "<tr>" + createTableCell(item.id, "id") +
    createTableCell(item.name, "name") +
    createTableCell(item.start_time, "start_time") + createTableCell(item.end_time, "end_time") +
    createTableLinkCell('/events?schedule_id='+item.id, "Events") + 
    createTableLinkCell('/items?schedule_id='+item.id, "Items") + 
    createTableLinkCell('/tasks?schedule_id='+item.id, "Tasks") +
    "<td>" + "<form method='DELETE' action='/diary/schedules/" + item.id + "/'>" +
    "<input type='submit'  onclick='deleteRow(this)'value='&#x2718;'></input>"
    "</form>"
    "</td></tr>";
    tbody.append(htmlStr)
}

function getTableOnSubmit(body){
    $(".resulttable tbody").empty();
    getResource(
        "http://localhost:5000/diary/schedules/",
        setRows);
}


$(document).ready(function (){
    getResource("http://localhost:5000/diary/schedules/", setRows)
    submitForm(getTableOnSubmit)
})