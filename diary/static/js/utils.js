'use strict';
const MASON = "application/vnd.mason+json"

function createTableRowsHtml(rowItems) {
    let htmlString = "<tr>";
    for (var item in rowItems) {
        htmlString += createTableCell(item);
    }
    return htmlString + "</tr>";
}

function createTableCell(item, className) {
    let tableRowString = "<td class='" + className + "' contentEditable='true'> " + item + " </td>";
    return tableRowString;
}


function createTableLinkCell(href, linkName = "Link") {
    let tableRowString = "<td>" + "<a href='" + href + "'>" + linkName + "</a>" + "</td>";
    return tableRowString;
}


function submitForm(onSuccessFunc) {
    let form = $("#new-post")
    form.submit(function (event) {
        event.preventDefault();
        let formData = form.serializeArray();
        let outData = {}
        for (var i=0; i < formData.length; i++){
            outData[formData[i]['name']] = formData[i]['value'];
        }
        console.log(outData)
        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: JSON.stringify(outData),
            contentType: MASON,
            processData: false,
            success: onSuccessFunc
        });
    });
}

function addActionToPostForm(ctrl) {
    let form = $("#new-post");
    form.attr('action', ctrl.self.href);
}

function getResource(href, successFunc) {
    $.ajax({
        url: href,
        success: successFunc
    })
}

// https://stackoverflow.com/questions/7731778/get-query-string-parameters-url-values-with-jquery-javascript
function getQueryParams() {
    $.urlParam = function (name) {
        var results = new RegExp('[\?&]' + name + '=([^&#]*)')
            .exec(window.location.search);

        return (results !== null) ? results[1] || 0 : false;
    }
}

function urlForSubCollection(subCollection){
    getQueryParams();
    return '/' + subCollection + "?schedule_id=" + $.urlParam('schedule_id')
}

function setNavLinks(){
    let eventLink = $('div.navigation #event-link');
    let itemLink = $('div.navigation #item-link');
    let taskLink = $('div.navigation #task-link');
    let schedulesLink = $('div.navigation #schedules-collection')
    if (eventLink.attr("href") != null){
        eventLink.attr("href", urlForSubCollection("events"));
    }
    if (taskLink.attr("href") != null){
        taskLink.attr("href", urlForSubCollection("tasks"));
    }
    if (itemLink.attr("href") != null){
        itemLink.attr("href", urlForSubCollection("items"));
    }
    if (schedulesLink.attr("href") != null){
        schedulesLink.attr("href", "/schedules/");
    }

}

function deleteRow(button){
    let form = $(button).parent();
    form.submit(function(event){
        event.preventDefault();
        $.ajax({
            url:form.attr("action"),
            method:"DELETE"
        });
        $(button).parents('tr').remove()    
    })
}

