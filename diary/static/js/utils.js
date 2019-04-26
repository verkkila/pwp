'use strict';


function createTableRowsHtml(rowItems){
    let htmlString = "<tr>";
    for (let item in rowItems){
        htmlString += createTableRow(item);
    }
    return htmlString + "</tr>";
}

function createTableRow(item){
    let tableRowString = "<td>" + item + "</td>";
    return tableRowString;
}

function submitForm(onSuccessFunc){
    let form = $("<form>");
    form.submitForm(function(event){
        event.preventDefault();
        let form = $("#new-post");
        let data = form.serialize();
        $.ajax({
            url:form.attr("action"),
            method:form.attr("method"),
            data:data,
            contentType:"application/vnd.mason+json",
            processData:false,
            success:onSuccessFunc
        });
    });
}

function addActionToPostForm(ctrl){
    let form = $("#new-post");
    form.attr('action',ctrl.self.href);
}


