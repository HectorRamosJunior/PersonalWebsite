/* Hector Ramos */
/* August 24, 2015 */

$(document).ready(function() {
  var $task_form = $("#task_form");
  var $textfield = $("#task_form input[name='text']");
  var $remove_task = $("#remove_task");

  $textfield.focus();

  $task_form.on("submit", function(event) {
    event.preventDefault();
    create_task();
  });

  $remove_task.on("submit", function(event) {
    event.preventDefault();
    delete_task();
  });


});



// AJAX for posting
function create_task() {
    var $textfield = $("#task_form input[name='text']");
    var $task_list = $("#task_list");


    $.ajax({
        //url : "create_task/",
        type : "POST", // http method
        data : { task_entry : $textfield.val(),
                 type : "create" }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $textfield.val(''); // remove the value from the input
            console.log(json);
            $task_list.append("<li name='" + json.task_pk + "'><input type='checkbox' name='" + json.task_pk + "'>" + json.text + "</li>");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
          alert("ERROR!");
        }
    });
};

function delete_task() {
    var $task_list = $("#task_list");
    var to_remove = [];

    $task_list.children().each(function() {
      if (($(this).children("input").is(":checked"))) {
        to_remove.push($(this).attr("name"));
      }
    });

    console.log(to_remove);


    $.ajax({
        //url : "create_task/",
        type : "POST", // http method
        data : { to_remove : to_remove ,
                 type : "remove" }, // data sent with the post request

        // handle a successful response
        success : function(json) {
          console.log(json);
          console.log(json.tasks_removed)
          var tasks_removed = json.tasks_removed;

          $task_list.children().each(function() {
            for (var i=0; i < tasks_removed.length; i++){
              if (($(this).children("input").attr("name") === tasks_removed[i])) {
                $(this).remove();
              }
            }
          });

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
          alert("ERROR!");
        }
    });
};



// Code below was copied to get CSRF tokens on AJAX.


// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
