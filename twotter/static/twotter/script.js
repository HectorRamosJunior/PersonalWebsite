/* Hector Ramos */
/* May 2nd, 2016 */

$(document).ready(function() {
    var $twoot_text = $("#twoot_text");
    var $twoot_button = $("#twoot_button");
    var $twoot_character_count = $("#twoot_character_count");

    // On first click and first click only, remove 140 character here text
    var click_count = 0;
    $twoot_text.click(function(){
        if (click_count === 0) {
            $twoot_text.empty();  
        }
        click_count++;
    });

    // If someone is getting close to 140 char limit, show them characters left
    // If someone exceeds the character limit, disable the submit button.
    $twoot_text.bind("DOMSubtreeModified", function(){
        var characters_left = 140 - $twoot_text.text().length

        // Handle if incorrect number of characters
        if (characters_left < 0 || characters_left === 140){
            $twoot_button.prop("disabled", true);

            if (characters_left < 0){
                $twoot_character_count.css("color", "red")
                $twoot_character_count.text(characters_left);
            }
        }
        // Handle correct number of characters in form
        else{
            $twoot_button.prop("disabled", false);

            if (characters_left <= 20){
                $twoot_character_count.css("color", "black")
                $twoot_character_count.text(characters_left);
            }
            else if (characters_left > 20){
                $twoot_character_count.empty();
            }  
        }
    });

    // Handle if someone presses enter in the twoot form
    $twoot_text.keypress(function (event) {
        // 13 is pressing enter
        if (event.keyCode == 13) {
            // Only press the button if the button is not disabled
            if ($twoot_button.prop("disabled") == false){
                $twoot_button.click();
            }
        }
     });

    // Handle if someone pushes the button to make a twoot in the twoot form
    $twoot_button.click(function(){
        make_twoot($twoot_text)
    });

});

function make_twoot($twoot_text) {
    // Ajax call to upload the score to the website's backend
    $.ajax({
        url : window.location.origin + "/twotter/make_twoot/",
        type : "POST", // http method
        data : { twoot_text : $twoot_text.text(), csrfmiddlewaretoken: window.CSRF_TOKEN },

        // handle a successful response
        success : function(json) {
          console.log("Worked!")
          add_twoot_to_feed(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
          console.log("Failed!")
        }
    });

    $twoot_text.empty();
};

// $task_list.append("<li name='" + json.task_pk + "'><input type='checkbox' name='" + json.task_pk + "'>" + json.text + "</li>");
function add_twoot_to_feed(json) {
    date = new Date(json.creation_date)
    // May 2, 2016, 4:07 p.m
    var month_names = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"];

    if (date.getHours() == 0) {
        var hour = 12;
        var am_or_pm = "a.m.";
    }
    else if (date.getHours() < 12) {
        var hour = date.getHours();
        var am_or_pm = "a.m.";
    }
    else if (date.getHours() == 12) {
        var hour = 12;
        var am_or_pm = "p.m.";
    }
    else {
        var hour = date.getHours() % 12;
        var am_or_pm = "p.m";
    }

    if (date.getMinutes() < 10){
        var minutes = "0" + date.getMinutes();
    }
    else {
        var minutes = date.getMinutes();
    }

    var creation_date = month_names[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear() + ', ' 
                        + hour + ':' + minutes + ' ' + am_or_pm;

    $(
      '<div class="w3-container w3-card-2 w3-white w3-round w3-margin" style="word-wrap:break-word;"><br>' +
        '<img src="' + json.avatar_url + '" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:60px">' +
        '<span class="w3-right w3-opacity">' + creation_date + '</span>' + 
        '<h4>' + json.display_name + '</h4><br>' +
        '<hr class="w3-clear">' +
        '<p>' + json.text + '</p>' +
        '<button type="button" class="w3-btn w3-theme-d1 w3-margin-bottom"><i class="fa fa-heart"></i> Favorite</button> ' +
        '<button type="button" class="w3-btn w3-theme-d2 w3-margin-bottom"><i class="fa fa-comment"></i>  Comment</button>' +
      '</div>'
    ).prependTo("#twoot_feed").hide().slideDown();
};