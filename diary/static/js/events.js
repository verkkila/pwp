'use strict';

function updateRow(event){
    let tbody = $(".resulttable tbody");
    let tableRowHtml = "<tr>" + createTableCell(event.id, "id") +
    createTableCell(event.name, "name") +
    createTableCell(event.duration, "duration") +
    createTableCell(event.note, "note") +
    "<td>" + "<form method=\"DELETE\" action=\"/diary/schedules/"  + $.urlParam("schedule_id") +
    "/events/" +  event.id + "/\">" +
    "<input type=\"submit\"  onclick=\"deleteRow(this)\"value=\"&#x2718;\"></input>" +
    "</form>" +
    "</td></tr>";
    tbody.append(tableRowHtml);
}

function createRows(body){
    let events = body.items;
    events.forEach(function(event) {
        updateRow(event);
    });
    let tableRows = ($("tbody tr td[contentEditable=true]"));
    tableRows.on("blur", function(){
        let outData = {};
        outData.name = $(this).parent().children(".name").html().trim();
        outData.duration = $(this).parent().children(".duration").html().trim();
        outData.note = $(this).parent().children(".note").html().trim();
        let url = "http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/events/" + $(this).parent().children(".id").html().trim() + "/";
        $.ajax({
            url:url,
            method:"PATCH",
            data:JSON.stringify(outData),
            contentType: MASON,
            success: null
        });
    });
}

function refreshTable(body){
    $(".resulttable tbody").empty();
    getResource("http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/events/", createRows);
}

$(document).ready(function (){
    setNavLinks();
    getQueryParams();
    $("#new-post").attr("action", "http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/events/")
    getResource("http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/events/", createRows);
    submitForm(refreshTable);
})