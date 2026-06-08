/* Initially based on https://codepen.io/tjezidzic/pen/LLWoLw */
/* Modified by Claude Sonnet 4.6 */

function makeCursor() {
  if (CURSOR === "block") {
    return "<span class='blinker blinker-block'></span>";
  } else if (CURSOR === "underline") {
    return "<span class='blinker blinker-underline'></span>";
  } else {
    return "<span class='blinker blinker-char'>" + CURSOR + "</span>";
  }
}

var allElements = document.getElementsByClassName("typeing");
for (var j = 0; j < allElements.length; j++) {
  (function(element) {
    var devTypeText = element.getAttribute("data-text") || "";
    var i = 0, isTag;
    (function type() {
      var text = devTypeText.slice(0, ++i);
      if (text === devTypeText) {
        element.innerHTML = text + (STAY_BLINKING ? makeCursor() : "");
        return;
      }
      element.innerHTML = text + makeCursor();
      var char = text.slice(-1);
      if (char === "<") isTag = true;
      if (char === ">") isTag = false;
      if (isTag) return type();
      setTimeout(type, REVEAL_SPEED_MS);
    })();
  })(allElements[j]);
}
