// define some welcome text
let welcome_text_1 = "Welcome! I'm QB. your virtual prtner in slef-quarantine."
let welcome_text_2 = "I can search for the latest health related to COVID-19, provide movie recommandations, find workout programs/video for you to follow, or suggest some meal pans/recipes to you! what would you like to do today?"

// on input/text enter--------------------------------------------------------------------------------------
$(".usrInput").on("keyup keypress", function(e) {
  var keyCode = e.keyCode || e.which;
  var text = $(".usrInput").val();
  if (keyCode === 13) {
    if (text == "" || $.trim(text) == "") {
      e.preventDefault();
      return false;
    } else {
      $(".usrInput").blur();
      setUserResponse(text);
      send(text);
      e.preventDefault();
      return false;
    }
  }
});

$(".delivery-button").on("click", function() {
  var text = $(".usrInput").val();
  if (text == "" || $.trim(text) == "") {
    return false;
  } else {
    $(".usrInput").blur();
    setUserResponse(text);
    send(text);
    return false;
  }
});

//------------------------------------- Set user response------------------------------------
function setUserResponse(val) {
  var UserResponse =
    "<img" + '><p class="userMsg">' + val + ' </p><div class="clearfix"></div>';
  $(UserResponse)
    .appendTo(".chats")
    .show("slow");
  $(".usrInput").val("");
  scrollToBottomOfResults();
  $(".suggestions").remove();
}

//---------------------------------- Scroll to the bottom of the chats-------------------------------
function scrollToBottomOfResults() {
  var terminalResultsDiv = document.getElementById("chats");
  terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
}

function send(message) {
  console.log("User Message:", message);
  $.ajax({
    url: "http://localhost:5005/webhooks/rest/webhook",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      message: message,
      sender: "Me",
    }),
    success: function(data, textStatus) {
      if (data != null) {
        setBotResponse(data);
      }
      console.log("Rasa Response: ", data, "\n Status:", textStatus);
    },
    error: function(errorMessage) {
      setBotResponse("");
      console.log("Error" + errorMessage);
    },
  });
}

//------------------------------------ Set bot response -------------------------------------
function setBotResponse(val) {
  setTimeout(function() {
    if (val.length < 1) {
      //if there is no response from Rasa
      msg = "I couldn't get that. Let' try something else!";

      var BotResponse =
        '<img class="botAvatar" src="./static/img/logo_only.svg"><p class="botMsg">' +
        msg +
        '</p><div class="clearfix"></div>';
      $(BotResponse)
        .appendTo(".chats")
        .hide()
        .fadeIn(1000);
    } else {
      //if we get response from Rasa
      for (i = 0; i < val.length; i++) {
        //check if there is text message
        if (val[i].hasOwnProperty("text")) {
          var BotResponse =
            '<img class="botAvatar" src="./static/img/logo_only.svg"><p class="botMsg">' +
            val[i].text +
            '</p><div class="clearfix"></div>';
          $(BotResponse)
            .appendTo(".chats")
            .hide()
            .fadeIn(1000);
        }

        //check if there is image
        if (val[i].hasOwnProperty("image")) {
          var BotResponse =
            '<div class="singleCard">' +
            '<img class="imgcard" src="' +
            val[i].image +
            '">' +
            '</div><div class="clearfix">';
          $(BotResponse)
            .appendTo(".chats")
            .hide()
            .fadeIn(1000);
        }

        //check if there is  button message
        if (val[i].hasOwnProperty("buttons")) {
          addSuggestion(val[i].buttons);
        }
      }
    }
    scrollToBottomOfResults();
  }, 500);
}


// ------------------------------------------ Suggestions -----------------------------------------------

function addSuggestion(textToAdd) {
  setTimeout(function() {
    var suggestions = textToAdd;
    var suggLength = textToAdd.length;
    $(
      ' <div class="singleCard"> <div class="suggestions"><div class="menu"></div></div></diV>'
    )
      .appendTo(".chats")
      .hide()
      .fadeIn(1000);
    // Loop through suggestions
    for (i = 0; i < suggLength; i++) {
      $(
        '<div class="menuChips" data-payload=\'' +
          suggestions[i].payload +
          "'>" +
          suggestions[i].title +
          "</div>"
      ).appendTo(".menu");
    }
    scrollToBottomOfResults();
  }, 1000);
}

// on click of suggestions, get the value and send to rasa (this one is not yet ready)
$(document).on("click", ".menu .menuChips", function() {
  var text = this.innerText;
  var payload = this.getAttribute("data-payload");
  console.log("button payload: ", this.getAttribute("data-payload"));
  setUserResponse(text);
  send(payload);
  $(".suggestions").remove(); //delete the suggestions
});

//send welcome text
$(document).ready(function(){
	setBotResponse([{"recipient_id":"Me","text":welcome_text_1}]);
	setBotResponse([{"recipient_id":"Me","text":welcome_text_2}]);
})
