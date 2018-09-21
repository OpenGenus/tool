// Discourse forum  popup and the live support feature goes here
var discourse_msg_active = false;
$(document).ready(function() {
  $(".forum_button").click(function() {
      console.log("clicked")
    if (discourse_msg_active == false) {
      $(".forum_popup_container").slideDown(300);
      discourse_msg_active = true;
    } else {
      $(".forum_popup_container").slideUp(300);
      discourse_msg_active = false;
    }
  });
  // Controls for the close button for this popup
  $(".forum_popup_close").click(function() {
    $(".forum_popup_container").slideUp(300);
    discourse_msg_active = false;
  });
});
