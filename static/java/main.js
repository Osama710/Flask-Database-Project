function archive(el) {
  let a = confirm("Are you sure?");
  if (a) {
    var row = el.closest("tr");
    var td = row.getElementsByTagName("td");
    var data = [];
    for (let i = 0; i < td.length - 1; i++) {
      data.push(td[i].innerHTML);
    }
    var header = [];
    var myTab = document.getElementById("second-table");

    // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
    for (i = 0; i < 1; i++) {
      // GET THE CELLS COLLECTION OF THE CURRENT ROW.
      var objCells = myTab.rows.item(i).cells;

      // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
      for (var j = 0; j < objCells.length - 1; j++) {
        header.push(objCells[j].innerText);
      }
    }

    var obj = {};
    for (var i = 0; i < header.length; i++) {
      obj[header[i]] = data[i];
    }

    const s = JSON.stringify(obj); // Stringify converts a JavaScript object or value to a JSON string
    $.ajax({
      url: "/deleteholdings",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(s),
      success: function (res) {
        alert("data archived");
        location.reload();
      },
    });
  }
}

function restore(el) {
  let a = confirm("Are you sure?");
  if (a) {
    var row = el.closest("tr");
    var td = row.getElementsByTagName("td");
    var data = [];
    for (let i = 0; i < td.length - 1; i++) {
      data.push(td[i].innerHTML);
    }
    var header = [];
    var myTab = document.getElementById("second-table");

    for (i = 0; i < 1; i++) {
      var objCells = myTab.rows.item(i).cells;
      for (var j = 0; j < objCells.length - 1; j++) {
        header.push(objCells[j].innerText);
      }
    }

    var obj = {};
    for (var i = 0; i < header.length; i++) {
      obj[header[i]] = data[i];
    }

    const s = JSON.stringify(obj);
    $.ajax({
      url: "/restoreholdings",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(s),
      success: function (res) {
        alert("data restored");
        location.reload();
      },
    });
  }
}

function archive1(el) {
  let a = confirm("Are you sure?");
  if (a) {
    var row = el.closest("tr");
    var td = row.getElementsByTagName("td");
    var data = [];
    for (let i = 0; i < td.length - 1; i++) {
      data.push(td[i].innerHTML);
    }
    var header = [];
    var myTab = document.getElementById("second-table");

    for (i = 0; i < 1; i++) {
      var objCells = myTab.rows.item(i).cells;
      for (var j = 0; j < objCells.length - 1; j++) {
        header.push(objCells[j].innerText);
      }
    }

    var obj = {};
    for (var i = 0; i < header.length; i++) {
      obj[header[i]] = data[i];
    }

    const s = JSON.stringify(obj);
    $.ajax({
      url: "/deletetransactions",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(s),
      success: function (res) {
        alert("data archived");
        location.reload();
      },
    });
  }
}

function restore1(el) {
  let a = confirm("Are you sure?");
  if (a) {
    var row = el.closest("tr");
    var td = row.getElementsByTagName("td");
    var data = [];
    for (let i = 0; i < td.length - 1; i++) {
      data.push(td[i].innerHTML);
    }
    var header = [];
    var myTab = document.getElementById("second-table");

    for (i = 0; i < 1; i++) {
      var objCells = myTab.rows.item(i).cells;
      for (var j = 0; j < objCells.length - 1; j++) {
        header.push(objCells[j].innerText);
      }
    }

    var obj = {};
    for (var i = 0; i < header.length; i++) {
      obj[header[i]] = data[i];
    }

    const s = JSON.stringify(obj);
    $.ajax({
      url: "/restoretransactions",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(s),
      success: function (res) {
        alert("data restored");
        location.reload();
      },
    });
  }
}

function addRecord(el) {
  var rows = el.closest("tr");
  var td = rows.getElementsByTagName("td");
  var data = [];
  for (let i = 0; i < td.length - 1; i++) {
    data.push(td[i].firstChild.value);
  }

  var header = [];
  var myTab = document.getElementById("second-table");

  for (i = 0; i < 1; i++) {
    var objCells = myTab.rows.item(i).cells;
    for (var j = 0; j < objCells.length - 1; j++) {
      header.push(objCells[j].innerText);
    }
  }

  var obj = {};
  for (var i = 0; i < header.length; i++) {
    obj[header[i]] = data[i];
  }

  const s = JSON.stringify(obj);
  $.ajax({
    url: "/addholdings",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(s),
    success: function (res) {
      alert("data added");
      location.reload();
    },
  });
}

function addRecord1(el) {
  var rows = el.closest("tr");
  var td = rows.getElementsByTagName("td");
  var data = [];
  for (let i = 0; i < td.length - 1; i++) {
    data.push(td[i].firstChild.value);
  }

  var header = [];
  var myTab = document.getElementById("second-table");

  for (i = 0; i < 1; i++) {
    var objCells = myTab.rows.item(i).cells;
    for (var j = 0; j < objCells.length - 1; j++) {
      header.push(objCells[j].innerText);
    }
  }

  var obj = {};
  for (var i = 0; i < header.length; i++) {
    obj[header[i]] = data[i];
  }

  const s = JSON.stringify(obj);
  $.ajax({
    url: "/addtransactions",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(s),
    success: function (res) {
      alert("data added");
      location.reload();
    },
  });
}
