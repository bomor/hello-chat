window.onload = function() {
  let nickname = localStorage.getItem("nickname");
  if (!nickname) {
    $('.ui.modal')
    .modal('show');
    $("#loginButton").on("click", function(){
      localStorage.setItem("nickname", $("#nickname").val());
      $('.ui.modal').modal('hide');
    })
  }

  let tabInUse;
  const inputData = $("#inputData");
  const sendButton = $("#sendButton");
  const searchButton = $("#searchButton")
  const searchInput = $("#searchInput")
  const searchResults = $("#searchResults")

  $('.ui.search')
    .search({
      apiSettings: {
        url: '//localhost:5000/search_messages/{query}'
      },
      fields: {
        results : 'items',
        title   : 'name',
        url     : 'html_url'
      },
      minCharacters : 3
    })
  ;

  $('#chatTabs a.item').on('click', function() {
    $(this)
      .addClass('active')
      .siblings()
      .removeClass('active');
    tabInUse = $(this);
    showMessages();
  })

fetch('/list_channels', {
    mode: 'cors'
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(channels) {
    buttonsHtml = channels.map((channel) => `<a class="item" id="${channel}-tab">${channel}</a>`);
    $("#chatTabs").html(buttonsHtml.join("\n"));
    tabInUse = $("#Food-tab");
    setInterval(showMessages, 1000);
    tabInUse.addClass("active");

  })
  .then(function() {
    $('#chatTabs a.item').on('click', function() {
      $(this)
        .addClass('active')
        .siblings()
        .removeClass('active');
      tabInUse = $(this);
      showMessages();
    })
  })
  .catch(function(error) {
    console.log('Request failed', error)
  });



  function showMessages(){
    fetch(`/messages_in_channel/${tabInUse.text()}`, {
        mode: 'cors'
      })
      .then(function(response) {
        return response.json();
      })
      .then(function(text2) {
        $("#messages").html(messagesParser(text2));
      })
      .catch(function(error) {
        console.log('Request failed', error);
      });
    }

  function messagesParser(text2){
    return text2.map(message => `${message.nickname}: ${message.message}`).join("<br>")
  }

  sendButton.on("click", sendMessage);

  $(document).keypress(function(e) {
      if (e.which == 13) {
        sendMessage();
        }
      });

  function sendMessage() {
      $.post(`/send_message/${tabInUse.text()}`, { "nickname" : localStorage.getItem("nickname") , "time" : "3:00" , "message" : inputData.val() }, function(result){ console.log(result) }).then(
        function(){
          showMessages();
          inputData.val("");
        });
  }
}
