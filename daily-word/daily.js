function play(audio_id) {
    var audio = document.getElementById(audio_id);
    audio.setAttribute("type", "audio/mpeg");
    audio.setAttribute("src", "/daily-word/" + audio_id + ".mp3");
}

var links = ["us", "uk"];
for (link in links) {
  var link_element = document.getElementById(links[link]);
  link_element.addEventListener("click", function(){play(links[link]+"_pronun");});
}

