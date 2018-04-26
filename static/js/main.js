/*
 * This is the Javascript file that makes requests to our controller.
 * We have prepared one API that makes requests in two unique ways
 * The filter option requests for data to be displayed and the download option 
 * requests for data to be in a downloadable form
 */



$( document ).ready(function() {
    get_records();

    $('#download-btn').click(function() {
        get_records("csv");
    });
    $('#filter-btn').click(function(e) {
        get_records(null);
    });
});

function get_records(format) {
    $("#result").addClass("loading")
    url = "/records"
    if (format) url += "?format=csv"
    $.ajax({
        url: url,
        method: "post",
        data: $('#queryform').serialize(),
        success: function(data) {
            display_data(data.records)
            $("#speech-count").html(comma_separate(data.count) + " speeches")
            $("#result").removeClass("loading")
        }
    });
    return false;
}

function display_data(data) {
    html = ""
    for (var i = 0; i < data.length; i++) {
         record = data[i]
         html += "<tr>"
         html += "<td>"+honorific(record[0])+"</td>" //honorific
         html += "<td>"+title_case(record[1])+"</td>" //speaker name
         html += "<td>"+record[2].substring(0,100) + "...</td>" //speech
         html += "<td>"+title_case(record[3])+"</td>" //hearing title
         html += "<td>"+record[4]+"</td>" //date
         html += "<td>"+title_case(record[5])+"</td>" //committee
         html += "<td>"+committee_type(record[6])+"</td>" // committee type
         html += "<td>"+party(record[7])+"</td>" //party
         html += "<td>"+chamber(record[8])+"</td>" //chamber
         html += "<td>"+if_null_blank(record[9])+"</td>" //state
         html += "<td>"+if_null_blank(record[10])+"</td>" // District
         html += "<td>"+pop_density(record[11])+"</td>" //Population density
         html += "</tr>"
    }
    $("#result-section").html(html)
}

function pop_density(val) {
    if (val == '5') return "Large City"
    if (val == '4') return "Medium City"
    if (val == '3') return "Small City"
    if (val == '2') return "Town"
    if (val == '1') return "Rural"
    return "-"
}

function chamber(val) {
    if (val == 'H') return "House"
    if (val == 'S') return "Senate"
    return "-"
}

function committee_type(val) {
    if (val == 'H') return "House"
    if (val == 'S') return "Senate"
    if (val == 'J') return "Joint"
    return "-"
}

function party(val) {
    if (val == 'D') return "Democrat"
    if (val == 'R') return "Republican"
    if (val == 'I') return "Independent"
    return "-"
}

function if_null_blank(val) {
    if (val) return val
    return "-"
}

function honorific(val) {
    if (!val) return ""
    return val
}
function title_case(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
const comma_separate = (x) => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}