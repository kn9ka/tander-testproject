/* global $ */
'use strict'

let locations
let regionlist = []
let citylist = []

// валидация класс 'phone-format'
$(document).ready(() => {
    $(".phone-format").keypress(function (e) {
        if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
          return false
        }
        
        let curchr = this.value.length
        let curval = $(this).val()
        
        if (curchr == 3 && curval.indexOf("(") <= -1) {
          $(this).val("(" + curval + ")" + "-")
        } else if (curchr == 4 && curval.indexOf("(") > -1) {
          $(this).val(curval + ")-")
        } else if (curchr == 5 && curval.indexOf(")") > -1) {
          $(this).val(curval + "-")
        } else if (curchr == 9) {
          $(this).val(curval + "-") 
          $(this).attr('maxlength', '14')
        }
    })
})

// заполнение списка регионов и городов
let appendLocations = () => {
    $.ajax({
        url: "/getLocations/",
        type:"GET",
        headers: {
            'Content-Type': 'application/json'
        },
        success: data => {
            locations = data
            for (let i = 0; i < data.length; i++) {
                regionlist.push(data[i][1])
                citylist.push(data[i][1])
                // заполнение выпадающего списка городов
                $('#city').append($("<option>", {text: data[i][0]}))
            }
            
            // уникальный список регионов
            let unique = Array.from(new Set(regionlist))
            unique.forEach( item => {
                $('#region').append($("<option>", {text: item}))
            })
        }
    })    
}

// валидация и отправка формы
let dataSubmit = () => {
    let dataForm = $("#dataForm").serializeArray()
    let isCorrect = true

    /* проверяем заполнено ли */
    isCorrect = checkError('#second_name')
    isCorrect = checkError('#first_name')
    isCorrect = checkError('#region')
    isCorrect = checkError('#city')
    isCorrect = checkError('#mobile')
    isCorrect = checkError('#email')
    isCorrect = checkError('#comment')
    
    if (isCorrect) {
            
        /* проверяем формат email */
            if ($('#email').val()) {
                let email = $('#email').val()
                let regex = new RegExp("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$")
                isCorrect = regex.test(email)
            }
            
            if (isCorrect) {
                $.ajax( {
                    url: "/submit",
                    type: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data: dataForm,
                    success: () => {
                        window.location.href = "/view/"
                        }
                })    
            } else {
                showError('#email', 'Ошбика в формате e-mail, пример: email@domain.com')
            }
    }

}

//триггер который срабатывает при выборе региона для заполнения списка городов
let onCityChange = () => {
    let region = $('#region').val()
    $('#region').find('#default-value').remove()
    $('#city').find('option').remove()
    for (var i = 0; i < locations.length; i++) {
        if(locations[i][1] === region) {
            citylist.push(locations[i][0])
            $('#city').append($("<option>", {text: locations[i][0]}))
        }
    }
}

// наполнение /view/
let getAllRows = () => {
    $.ajax({
        url: '/getAllRows/',
        type: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        success: data => {
            data.forEach( row => {
                $("#root > tbody:last-child").append(("<tr></tr>"))
                for (var i = 1; i< row.length; i++){
                    $("#root > tbody:last-child").append($("<td></td>", { text: row[i]}))
                }
                $("#root > tbody:last-child").append($("<button>",
                    {row: row[0], class: 'btn btn-outline-danger' ,text: 'delete row', onclick: "deleteRow(" + row[0]+ ")"}))
            })
        }
    })
}

// наполнение /stat/
let getCommentsByRegion = () => {
    $.ajax({
    url: '/getCommentsByRegion/',
    type: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    success: data => {
        data.forEach( row => {
            $("#root > tbody:last-child").append(("<tr></tr>"))
            $("#root > tbody:last-child").append("<td><a href='/stat/" + row[2] + "/' >" + row[0] + "</a></td>")
            $("#root > tbody:last-child").append($("<td></td>", {text: row[1]}))
        })
    }
    })
}

// наполнение /stat/{region id}/
let getCommentsByCity = () => {
    let regionId = window.location.pathname.split('/')[2]

    $.ajax({
        url: '/getCommentsByCity/',
        type: 'POST',
        data: {regionId},
        headers: {
            'Content-Type': 'application/json'
        },
        success: data => {
            data.forEach(row => {
                $("#root > tbody:last-child").append(("<tr></tr>"))
                $("#root > tbody:last-child").append("<td> " + row[0] + "</td>")
                $("#root > tbody:last-child").append($("<td></td>", {text: row[1]}))
            })
        }
    })
}

// удаление строки по rowId из БД
let deleteRow = (rowId) => {
    $.ajax({
        url: '/delete/',
        type: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        data: {rowId},
        success: () => {
            window.location.reload()
        }
    })
}

let showError = (element, errorMessage) => {
    $(element).addClass("is-invalid")
    if (errorMessage) {
        $(element).next("div").text(errorMessage)
    }
}

let resetError = (element) => {
    $(element).removeClass("is-invalid")
}

let checkError = (element, errorMessage) => {
    resetError(element)
    if (!$(element).val()) {
        showError(element, errorMessage)
        return false
    }
    if ($(element).val() == 'Выберите регион' || ($(element).val()) == 'Выберите город') {
        errorMessage = 'Выберите регион из списка'
        showError(element, errorMessage)
        return false
    }
    return true
}