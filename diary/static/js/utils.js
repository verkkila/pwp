'use strict';
const MASON = "application/vnd.mason+json"

function createTableRowsHtml(rowItems) {
    let htmlString = "<tr>";
    for (var item in rowItems) {
        htmlString += createTableRow(item);
    }
    return htmlString + "</tr>";
}

function createTableRow(item) {
    let tableRowString = "<td> " + item + " </td>";
    return tableRowString;
}

function createTableLinkRow(href, linkName = "Link") {
    let tableRowString = "<td>" + "<a href='" + href + "'>" + linkName + "</a>" + "</td>";
    return tableRowString;
}

function submitForm(onSuccessFunc) {
    let form = $("<form>");
    form.submitForm(function (event) {
        event.preventDefault();
        let form = $("#new-post");
        let data = form.serialize();
        $.ajax({
            url: form.attr("action"),
            method: form.attr("method"),
            data: data,
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
    if (eventLink.attr("href") != null){
        eventLink.attr("href", urlForSubCollection("events"));
    }
    if (taskLink.attr("href") != null){
        taskLink.attr("href", urlForSubCollection("tasks"));
    }
    if (itemLink.attr("href") != null){
        itemLink.attr("href", urlForSubCollection("items"));
    }

}

