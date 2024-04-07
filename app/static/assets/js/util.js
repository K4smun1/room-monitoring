const showStatus = (function () {
    let alerted = false;

    return function (msg, val) {
        if (!alerted && !val) {
            alerted = true;
            alert(msg);
        } else if (alerted && val) {
            alerted = false;
            alert(msg);
        }
    }
  })();