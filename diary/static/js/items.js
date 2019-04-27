function setRows(body){
    let items = body.items;
    let tbody = $(".resulttable tbody");
    items.forEach(function(item) {
        updateRow(item)
    });
}

function updateRow(item){
    let tbody = $(".resulttable tbody");
    htmlStr = "<tr>" + createTableCell(item.name) +
    createTableCell(item.value) +
    "<td>" + "<form method='DELETE' action='/diary/schedules/"  + $.urlParam('schedule_id')  + 
    "/items/" +  item.id + "/'>" +
    "<input type='submit'  onclick='deleteRow(this)'value='&#x2718;'></input>"
    "</form>"
    "</td></tr>";
    tbody.append(htmlStr)
}



function getTableOnSubmit(body){
    $(".resulttable tbody").empty();
    getResource(
        "http://localhost:5000/diary/schedules/" + $.urlParam('schedule_id') + "/items/",
        setRows);
}

$(document).ready(function (){
    getQueryParams();
    setNavLinks();
    $("#new-post").attr("action", "http://localhost:5000/diary/schedules/" + $.urlParam('schedule_id') + "/items/")
    getResource(
        "http://localhost:5000/diary/schedules/" + $.urlParam('schedule_id') + "/items/",
        setRows);
    submitForm(getTableOnSubmit)
})