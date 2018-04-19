/*
 * This is the Javascript file that makes requests to our controller.
 * We have prepared one API that makes requests in two unique ways
 * The filter option requests for data to be displayed and the download option 
 * requests for data to be in a downloadable form
 */


//$('#filter-btn').click(function() {
//	//Reload the page to display the new data.
//	//You could optionally work with Ajax
//	window.location.href="/speakers?name=" + $("#speaker").val() + "&year=" + $("#year").val()
//});
//
//$('#download-btn').click(function() {
//	window.location.href="/speakers?format=csv&name=" + $("#speaker").val() + "&year=" + $("#year").val()
//});


$.ajax({
    url: "/records",
    success: function(data) {
        display_data(data.records)
    }
});

function display_data(data) {
    html = ""
    for (var i = 0; i < data.length; i++) {
         record = data[i]
         html += "<tr>"
         html += "<td>"+record['honorific']+"</td>"
         html += "<td>"+record['full_name']+"</td>"
         html += "<td>"+record['text'] + "</td>"
         html += "<td>"+record['hearing_title']+"</td>"
         html += "<td>"+record['date']+"</td>"
         html += "<td>"+record['committee_name']+"</td>"
         html += "<td>"+record['type']+"</td>"
         html += "<td>"+record['party']+"</td>"
         html += "<td>"+record['chamber']+"</td>"
         html += "<td>"+record['state_name']+"</td>"
         html += "<td>"+record['district']+"</td>"
         html += "<td>"+record['density_quintile']+"</td>"
         html += "</tr>"
    }
    $("#result-section").html(html)
}