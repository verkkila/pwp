function setRows(body){
    let items = body.items;
    items.forEach(function(item) {
        updateRow(item)
    });
    let tableRows = ($('tbody tr td[contentEditable=true]'));
    tableRows.on("blur", function(){
        let outData = {}
        outData.name = $(this).parent().children('.name').html().trim()
        outData.value = $(this).parent().children('.value').html().trim()
        let url = "http://localhost:5000/diary/schedules/" + $.urlParam('schedule_id') + 
        '/items/' + $(this).parent().children('.id').html().trim() + '/';
        $.ajax({
            url:url,
            method:"PATCH",
            data:JSON.stringify(outData),
            contentType: MASON,
            success: null
        });
    })
}

function updateRow(item){
    let tbody = $(".resulttable tbody");
    htmlStr = "<tr>" + createTableCell(item.id, 'id') + 
    createTableCell(item.name, 'name') +
    createTableCell(item.value, 'value') +
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