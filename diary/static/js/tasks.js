'use strict';

function updateRow(task){
    let tbody = $(".resulttable tbody");
    let tableRowHtml = "<tr>" + createTableCell(task.id, "id") + 
    createTableCell(task.name, "name") +
    createTableCell(task.priority, "priority") +
    createTableCell(task.goal, "goal") +
    createTableCell(task.result, "result") +
    "<td>" + "<form method=\"DELETE\" action=\"/diary/schedules/"  + $.urlParam("schedule_id")  +
    "/tasks/" +  task.id + "/\">" +
    "<input type=\"submit\"  onclick=\"deleteRow(this)\"value=\"&#x2718;\"></input>" +
    "</form>" +
    "</td></tr>";
    tbody.append(tableRowHtml);
}

function createRows(body){
    let tasks = body.items;
    tasks.forEach(function(task) {
        updateRow(task);
    });
    let tableRows = ($("tbody tr td[contentEditable=true]"));
    tableRows.on("blur", function(){
        var outData = new Object();
        outData.name = $(this).parent().children(".name").html().trim();
        outData.priority = parseInt($(this).parent().children(".priority").html().trim());
        outData.goal = $(this).parent().children(".goal").html().trim();
        let url = "http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/tasks/" + $(this).parent().children(".id").html().trim() + "/";
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
    getResource("http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/tasks/", createRows);
}

$(document).ready(function (){
    setNavLinks();
    getQueryParams();
    $("#new-post").attr("action", "http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/tasks/");
    getResource("http://localhost:5000/diary/schedules/" + $.urlParam("schedule_id") + "/tasks/", createRows);
    submitForm(refreshTable);
})