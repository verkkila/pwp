function setRows(body){
    let items = body.items;
    let tbody = $(".resulttable tbody");
    items.forEach(function(item) {
        tbody.prepend("<tr>")
        tbody.append(createTableRow(item.name));
        tbody.append(createTableRow(item.value));
        tbody.append("</tr>")
    });
}


$(document).ready(function (){
    getQueryParams();
    setNavLinks();
    getResource(
        "http://localhost:5000/diary/schedules/" + $.urlParam('schedule_id') + "/items/",
        setRows);
})