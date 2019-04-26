'use strict';

function setRows(body){
    let items = body.items;
    let tbody = $(".resulttable tbody");
    items.forEach(function(item) {
        tbody.prepend("<tr>")
        tbody.append(createTableRow(item.name));
        tbody.append(createTableRow(item.start_time));
        tbody.append(createTableRow(item.end_time));
        tbody.append(createTableLinkRow('/events?schedule_id='+item.id, "Events"))
        tbody.append(createTableLinkRow('/items?schedule_id='+item.id, "Items"))
        tbody.append(createTableLinkRow('/tasks?schedule_id='+item.id, "Tasks"))
        tbody.append("</tr>")
    });
}

$(document).ready(function (){
    getResource("http://localhost:5000/diary/schedules/", setRows)
})