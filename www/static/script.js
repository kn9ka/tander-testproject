console.log('script loaded')

/* AJAX */
var list

$(document).ready ( function () {
    $.ajax({
        url: "/city",
        type:"GET",
        headers: {
            'Content-Type': 'application/json'
        },
        success: function (data) {
            list = data
            console.log(data)
            var regionlist = []

            for (var i = 0; i < data.length; i++) {
                regionlist.push(data[i][1])
                $('#citylist').append($("<option></option>", {value: data[i][0]}))
            }
            var unique = Array.from(new Set(regionlist))
            unique.forEach(function(item){
                $('#regionlist').append($("<option></option>", {value: item}))
            })
        }
    })
    
    $.ajax({
        url: "/getAllRows",
        type: "GET",
        headers: {'Content-Type': 'application/json'},
        success: function (dataRow) {
            console.log(dataRow)
        }
    })
})

function dataSubmit() {
    var dataForm = $("#dataForm").serializeArray()
    var hilight_css = {"border-color":"red"}
    if (!$('#first_name').val()) {
        $('#first_name').css(hilight_css) 
    }
    if (!$('#second_name').val()) {
        $('#second_name').css(hilight_css) 
    }
    if (!$('#comment').val()) {
        $('#comment').css(hilight_css) 
    }
    $.ajax( {
        url: "/submit",
        type: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        data: dataForm,
        success: function() {
            alert('data submitted')
        }
    })
    }
    

function onCityChange () {
    var citylist = []
    var region = $('#region').val()
    
    $('#citylist').find('option').remove()
    
    for (var i = 0; i < list.length; i++) {
        if(list[i][1] === region) {
            citylist.push(list[i][0])
            $('#citylist').append($("<option></option>", {value: list[i][0]}))
        }
    }
}