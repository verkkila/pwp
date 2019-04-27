'use strict';

function setRows(body){
    let items = body.items;
    items.forEach(function(item) {
        updateRow(item)
    });
}

function updateRow(item){
    let tbody = $(".resulttable tbody");
    tbody.append("<tr>")
    tbody.append(createTableCell(item.name));
    tbody.append(createTableCell(item.start_time));
    tbody.append(createTableCell(item.end_time));
    tbody.append(createTableLinkRow('/events?schedule_id='+item.id, "Events"))
    tbody.append(createTableLinkRow('/items?schedule_id='+item.id, "Items"))
    tbody.append(createTableLinkRow('/tasks?schedule_id='+item.id, "Tasks"))
    tbody.append("<td><button onclick='deleteItem(item.id)'>&#10006;</button></td>");
    tbody.append("</tr>")
}

$(document).ready(function (){
    getResource("http://localhost:5000/diary/schedules/", setRows)
    submitForm(updateRow)
})