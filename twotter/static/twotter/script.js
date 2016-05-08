/* Hector Ramos */
/* May 2nd, 2016 */

$(document).ready(function() {
    var $twoot_text = $("#twoot_text");
    var $twoot_button = $("#twoot_button");
    var $twoot_character_count = $("#twoot_character_count");

    // For all twoots on page generation, check each for image/youtube urls and append 
    // image/iframe tags to the twoot if they are detected
    $(".twoot_text").each(function() {
        convert_twoot_urls($(this));
    });

    // On first click and first click only, remove 140 character here text
    var click_count = 0;
    $twoot_text.click(function(){
        if (click_count === 0) {
            $twoot_text.empty();  
        }
        click_count++;
    });

    // Handles Twoot form character count and disables twoot button if character count is invalid
    $twoot_text.bind("propertychange change click keyup input paste", function(){
        var characters_left = 140 - this.value.length

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

    // If someone presses enter in the twoot form, submit the twoot (Arguable if wanted?)
    $twoot_text.keypress(function (event) {
        // 13 is pressing enter
        if (event.keyCode == 13) {
            event.preventDefault();

            // Only press the button if the button is not disabled
            if ($twoot_button.prop("disabled") == false){
                $twoot_button.click();
            }
        }
     }); 

    // Make twoot with cvurrent twoot text form if user clicks twoot button
    $twoot_button.click(function(){
        make_twoot($twoot_text)
    });

    // Favorite twoots, listens for newly created DOM twoot elements
    $(document).on("click", ".favorite_button", function(){
        favorite_twoot(this.id);
    })

    // Retwoot twoots, listens for newly created DOM twoot elements
    $(document).on("click", ".retwoot_button", function(){
        retwoot_twoot(this.id);
    })

    // Toggle the dropdown menus for the twoots, listens for newly created DOM twoot elements
    $(document).on("click", ".dropdown_toggle", function(){
        $(this).next().show();
    })

    // If someone clicks outside the twoot dropdown menu, make sure all twoot menus are closed
    $(document).bind("click", function(event){
        if (!$(event.target).is(".dropdown_toggle")) { 
            $(".dropdown_toggle").each(function(){
                $(this).next().hide();
            });
        }
    });

});

// Makes an AJAX call with the given twoot text in the form to create a new twoot.
// If successful, it empties the twoot form and dynamically creates the twoot on the page via add_twoot_to_feed
function make_twoot($twoot_text) {
    // Ajax call to upload the score to the website's backend
    $.ajax({
        url : window.location.origin + "/twotter/make_twoot/",
        type : "POST", // http method
        data : { twoot_text : $twoot_text.val(), csrfmiddlewaretoken: window.CSRF_TOKEN },

        // handle a successful response
        success : function(json) {
            console.log("AJAX Call Successful!")
            add_twoot_to_feed(json);
            $("#twoot_count").html('<i class="fa fa-file-text-o w3-margin-right w3-text-theme"></i> ' + json.twoot_count + ' Twoots')
            $("#twoot_character_count").empty();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("AJAX Call Failed!")
        }
    });

    // Empty input field text
    $twoot_text.val("");
};

// Makes an AJAX call to favorite/unfavorite the given twoot on the page.
// If successful, the twoot's favorite button number will change dynamically 
function favorite_twoot(twoot_pk) {
    twoot_pk = twoot_pk.replace('favorite_', '');

    // Ajax call to upload the score to the website's backend
    $.ajax({
        url : window.location.origin + "/twotter/favorite_twoot/",
        type : "POST", // http method
        data : { twoot_pk : twoot_pk, csrfmiddlewaretoken: window.CSRF_TOKEN },

        // handle a successful response
        success : function(json) {
            console.log("AJAX Call Successful!")
            if (json.favorite_count > 0) {
                $("#favorite_" + twoot_pk).html('<i class="fa fa-heart"></i> ' + json.favorite_count)
            }
            else if (json.favorite_count <= 0){
                $("#favorite_" + twoot_pk).html('<i class="fa fa-heart"></i> ')
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("AJAX Call Failed!")
        }
    });
};

// Makes an AJAX call to retwoot/unretwoot the given twoot on the page.
// If successful, the twoot's retwoot button number will change dynamically
function retwoot_twoot(twoot_pk) {
    twoot_pk = twoot_pk.replace('retwoot_', '');

    // Ajax call to upload the score to the website's backend
    $.ajax({
        url : window.location.origin + "/twotter/retwoot_twoot/",
        type : "POST", // http method
        data : { twoot_pk : twoot_pk, csrfmiddlewaretoken: window.CSRF_TOKEN },

        // handle a successful response
        success : function(json) {
            console.log("AJAX Call Successful!")
            if (json.retwoot_count > 0) {
                $("#retwoot_" + twoot_pk).html('<i class="fa fa-retweet"></i> ' + json.retwoot_count)
            }
            else if (json.retwoot_count <= 0){
                $("#retwoot_" + twoot_pk).html('<i class="fa fa-retweet"></i> ')
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("AJAX Call Failed!")
        }
    });
};

// Makes an AJAX call to delete the given twoot on the page.
// If successful, the twoot will slide up and be deleted from the user's feed dynamically
function delete_twoot(twoot_pk) {
    twoot_pk = twoot_pk.replace('delete_', '');
    
    // Ajax call to upload the score to the website's backend
    $.ajax({
        url : window.location.origin + "/twotter/delete_twoot/",
        type : "POST", // http method
        data : { twoot_pk : twoot_pk, csrfmiddlewaretoken: window.CSRF_TOKEN },

        // handle a successful response
        success : function(json) {
            console.log("AJAX Call Successful!")
            delete_twoot_from_feed(json);
            if (json.username != "admin") {
                $("#twoot_count").html('<i class="fa fa-file-text-o w3-margin-right w3-text-theme"></i> ' + json.twoot_count + ' Twoots')
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("AJAX Call Failed!")
        }
    });
};

// Dynamically adds the new twoot from make_twoot AJAX's call to the feed if successful.
// Uses the json data returned from the AJAX call to dynamically create an identical twoot to the others.
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

    var twoot = '<div class="w3-container w3-card-2 w3-white w3-round w3-margin twoot_display" id="twoot_' + json.pk + '"><br>' +
                '<a href="' + window.location.origin + '/twotter/' + json.username + '/">' + 
                '<img src="' + json.avatar_url + '" alt="Avatar" class="w3-left w3-circle w3-margin-right twotter_link" style="width:60px"></a>' +
                '<span class="w3-right w3-opacity">' + 
                '<li class="w3-right w3-dropdown-click">' +
                '<i class="fa fa-caret-down dropdown_toggle" aria-hidden="true"></i>' +
                '<div class="w3-dropdown-content w3-white w3-card-4" style="right: 0;">' + 
                '<a href="javascript:void(0)" id="delete_' + json.pk + '" onclick="delete_twoot(this.id)">Delete</a>' + 
                '</div>' + 
                '</li><br>' + 
                '<a href="' +  window.location.origin + '/twotter/twoot/' + json.pk + '/" class="twotter_link">' +  creation_date + '</a></span>' + 
                '<h4><a href="' + window.location.origin + '/twotter/' + json.username + '/" class="twotter_link">' + json.display_name + '</a></h4><br>' +
                '<hr class="w3-clear">' +
                '<p class="twoot_text"></p>' +
                '<button type="button" class="w3-btn w3-theme-d1 w3-margin-bottom retwoot_button" id="retwoot_' + json.pk + '"><i class="fa fa-retweet"></i> </button> ' +
                '<button type="button" class="w3-btn w3-theme-d1 w3-margin-bottom favorite_button" id="favorite_' + json.pk + '"><i class="fa fa-heart"></i> </button> ' +
                '</div>'; 

    $(twoot).prependTo("#twoot_feed").hide();

    $("#twoot_" + json.pk).find(".twoot_text").text(json.text);     // Avoid HTML injection!
    convert_twoot_urls($("#twoot_" +  json.pk).find(".twoot_text"));    // Check for image/youtube links
    $("#twoot_" +  json.pk).slideDown('slow');                      // Finally, add twoot to feed dynamically!
};

// Dynamically removes the new twoot from delete_twoot AJAX's call to the feed if successful.
// Uses the json data returned from the AJAX call to specify which twoot to delete dynamically.
function delete_twoot_from_feed(json) {
    var $twoot = $("#twoot_" + json.pk);

    $twoot.slideUp('slow', function() {
        $twoot.remove();    
    });
};

// Adds img elements of the photos contained within the given twoot
function convert_twoot_urls(twoot) {
    var url_regex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    var photo_regex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|]).(?:jpg|gif|png)/ig;
    var youtube_regex = /(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?/;

    var url_url = $(twoot).text().match(url_regex);
    var url_photo = $(twoot).text().match(photo_regex);
    var url_youtube = $(twoot).text().match(youtube_regex);

    if (url_photo != null) {
        $.each(url_photo, function(key, value) {
           var convert_photo ='<img src="' + value + '" style="max-width:100%; max-height:100%;"><br><br>';
           $(twoot).after(convert_photo);
        });
    }

    if (url_youtube != null) {
        $.each(url_youtube, function(key, value) {
            if (value.length == 11) {
                var convert_youtube = '<iframe src="//www.youtube.com/embed/' + value + '" frameborder="0" allowfullscreen></iframe><br><br>';
                $(twoot).after(convert_youtube);
            }
        });
    }
};