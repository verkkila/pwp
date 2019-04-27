'use strict';

function setRows(body){
    let items = body.items;
    items.forEach(function(item) {
        updateRow(item)
    });
}

function updateRow(item){
    let tbody = $(".resulttable tbody");
    let htmlStr = "<tr>" + createTableCell(item.name) +
    createTableCell(item.start_time) + createTableCell(item.end_time) +
    createTableLinkCell('/events?schedule_id='+item.id, "Events") + 
    createTableLinkCell('/items?schedule_id='+item.id, "Items") + 
    createTableLinkCell('/tasks?schedule_id='+item.id, "Tasks") +
    "<td>" + "<form method='DELETE' action='/diary/schedules/" + item.id + "/'>" +
    "<input type='submit'  onclick='deleteRow(this)'value='&#x2718;'></input>"
    "</form>"
    "</td></tr>";
    tbody.append(htmlStr)
}




$(document).ready(function (){
    getResource("http://localhost:5000/diary/schedules/", setRows)
    submitForm(updateRow)
})