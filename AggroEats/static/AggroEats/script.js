/* Hector Ramos */
/* August 24, 2015 */

$(document).ready(function() {
  var $body = $("body");
  
  // Add aggro and cricket to the document
  $body.append("<div id='aggro'><span id='score'></span></div>");
  $body.append("<div id='cricket'></div>");
  $body.append("<div id='eaten'></div>");

  // Set the jquery variables for future use and readability
  var $cricket = $("#cricket");
  var $aggro = $("#aggro");
  var $score = $("#score");
  var $eaten = $("#eaten");

  // Load game audio tags from DOM for future use
  var $biteSound = $("#bite").get(0);
  var $missedSound = $("#bzzt").get(0);

  // Stored in objects to be able to be passed by reference
  var scoreObj = {curr: 0, max: 0};
  var timeObj = {timer: 0, milisecs: 5000, $missedSound: $missedSound};

  // When the cricket is clicked, update the score and move it
  $cricket.click(function() {
    endAndStartTimer(timeObj, scoreObj);
    $cricket.hide();  // No Cheaters!

    playBiteSound($biteSound);
    moveCricket($cricket, $eaten, scoreObj);
    updateScore($score, scoreObj);

    $cricket.show();
  });

});


// Plays the bite sound. Interrupts and stops the previous sound if playing
function playBiteSound($biteSound) {
    $biteSound.pause();
    $biteSound.currentTime = 0;
    $biteSound.play(); 
};

// Moves the cricket element randomly on the page
function moveCricket($cricket, $eaten) {
  var left = 0;
  var bottom = 0;

  // Move bite element to current cricket location since it was eaten
  // Also start a timer to hide the bite graphic after .1 seconds
  $eaten.css({bottom: $cricket.css("bottom"), left: $cricket.css("left")});
  $eaten.show();
  window.setTimeout(function() { $eaten.hide(); }, 100);

  // Make sure the cricket doesn't overlap with aggro
  while (left < 15 && bottom < 15) {
    left = Math.floor(Math.random() * (90 + 1));
    bottom = Math.floor(Math.random() * (90 + 1));
  }

  // Repositon the cricket on the webpage to its randomized position
  $cricket.css({bottom: bottom + "%", left: left + "%"});
};

// Updates the current score and max score if necessary, changes $score's text
function updateScore($score, scoreObj) {
  scoreObj.curr++;

  if (scoreObj.curr > scoreObj.max) {
    scoreObj.max = scoreObj.curr
  }

  $score.html("<b>Score: " + scoreObj.curr + "<br>Max: " + scoreObj.max + "</b>");
};

// Plays the missed sound, resets score and moves cricket to original position
function restartGame(timeObj, scoreObj) {
  timeObj.$missedSound.play()

  var endString = "Time's up! "
  endString += "Your score was " + scoreObj.curr
  endString +=  ", your max this session is " + scoreObj.max + "."
  endString += "<br>Click on the cricket to start the game again!"
  $("#leaderboard").find("p").html(endString)

  // Ajax call to upload the score to the website's backend
  $.ajax({
    url : "create_score/",
    type : "POST", // http method
    data : { score : scoreObj.curr, csrfmiddlewaretoken: window.CSRF_TOKEN },

    // handle a successful response
    success : function(json) {
      updateLeaderboard()
      $('#leaderboard').modal('show');
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
      console.log("Failed to save score data. Is the user logged in?")
      updateLeaderboard()
      $('#leaderboard').modal('show');
    }
  });

  // Reset the timer and current score to orginal values
  scoreObj.curr = 0;
  timeObj.milisecs = 5000;

  // Reset the game elements to their original positions
  $("#score").html("<b>Score: "+ scoreObj.curr +"<br>Max: "+ scoreObj.max +"</b>");
  $("#cricket").css({bottom: "90%", left: "90%"});
  $("#eaten").css({bottom: "90%", left: "90%"});
};

// Starts the timer between cricket clicks and ends game if the timer runs out
function endAndStartTimer(timeObj, scoreObj) {
  window.clearTimeout(timeObj.timer);
  timeObj.milisecs = timeObj.milisecs / 1.05    // Reduce miliseconds for timeout
  timeObj.timer = window.setTimeout(function() { restartGame(timeObj, scoreObj); }, timeObj.milisecs);
};

// Updates the leaderboard modal on the website
function updateLeaderboard() {
  // Ajax call to retrieve the top 10 scores for the leaderboard
  $.ajax({
    url : "leaderboard/",
    type : "POST", // http method
    data : { csrfmiddlewaretoken: window.CSRF_TOKEN },

    // handle a successful response
    success : function(json) {
      $("#topScores").find("tbody").empty();

      // Appends the top scores to the leaderboard html table
      for (i = 0; i < json.length; i++){
        var tableRow = "<tr>";

        // Add rank
        tableRow += "<td>" + (i+1) + "</td>";
        // Add username
        tableRow += "<td>" + json[i][0] + "</td>";
        // Add score
        tableRow += "<td>" + json[i][1] + "</td>"
        // Close row
        tableRow += "</tr>"

        $("#topScores").find('tbody').append(tableRow);
      }
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
      console.log("Failed to get leaderboard data!");
    }
  });
};
