function doGet(e) {
    if (!e.parameter.action) {
        e.parameter.action = "default";
    }

    const action = e.parameter.action;
    if (action == "default") {
        return defaultEndpoint(e);
    } else if (action == "data") {
        return getData(e);
    } else {
        return ContentService.createTextOutput(
            JSON.stringify({ error: "action not found" })
        ).setMimeType(ContentService.MimeType.JSON);
    }
}

function defaultEndpoint(e) {
    if (!e.parameter.targetSheet) {
        return ContentService.createTextOutput(JSON.stringify([])).setMimeType(
            ContentService.MimeType.JSON
        );
    }
    var delta = undefined;
    if (e.parameter.delta) {
        delta = e.parameter.delta;
    }

    const targetSheet = e.parameter.targetSheet;

    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    if (targetSheet != "ALL") {
        const sheet = spreadsheet.getSheetByName(targetSheet);
        const data = process(sheet, delta);
        return ContentService.createTextOutput(JSON.stringify(data)).setMimeType(
            ContentService.MimeType.JSON
        );
    } else if (targetSheet == "ALL") {
        var allData = [];
        var date = undefined;
        spreadsheet.getSheets().forEach((s) => {
            objResult = process(s, delta);
            allData = allData.concat(objResult.Result);
            date = objResult.Date;
        });
        return ContentService.createTextOutput(
            JSON.stringify({
                Result: allData,
                Date: date,
            })
        ).setMimeType(ContentService.MimeType.JSON);
    }
}

function getData(e) {
    if (!e.parameter.nim) {
        return ContentService.createTextOutput(
            JSON.stringify({ error: "nim not found" })
        ).setMimeType(ContentService.MimeType.JSON);
    }

    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const nim = parseInt(e.parameter.nim);
    for (const sheet of spreadsheet.getSheets()) {
        const data = sheet.getDataRange().getValues();
        const normalized = normalizeData(data);
        const filtered = normalized.filter((x) => x["NIM"] == nim);
        if (filtered.length != 0) {
            return ContentService.createTextOutput(JSON.stringify(filtered[0])).setMimeType(
                ContentService.MimeType.JSON
            );
        }
    }
    return ContentService.createTextOutput(JSON.stringify({ error: "nim not found" })).setMimeType(
        ContentService.MimeType.JSON
    );
}

const months = {
    0: "January",
    1: "February",
    2: "March",
    3: "April",
    4: "May",
    5: "June",
    6: "July",
    7: "August",
    8: "September",
    9: "October",
    10: "November",
    11: "December",
};

function process(sheet, delta) {
    const data = sheet.getDataRange().getValues();
    const jsonData = birthday(normalizeData(data), delta);
    dateStr = jsonData.Date.getDate() + " " + months[jsonData.Date.getMonth()];
    jsonData.Date = dateStr;
    return jsonData;
}

function normalizeData(data) {
    const headers = data[0];
    const raw_data = data.slice(1);
    let json = [];
    raw_data.forEach((d) => {
        let object = {};
        for (let i = 0; i < headers.length; i++) {
            if (headers[i] == "Ultah") {
                object[headers[i]] = new Date(d[i]);
            } else {
                object[headers[i]] = d[i];
            }
        }
        if (object["Ultah"].getFullYear() >= 1990) {
            json.push(object);
        }
    });
    return json;
}

function birthday(data, delta) {
    var pickDate = new Date();
    var d;
    if (delta) {
        d = parseInt(delta);
    } else {
        d = 0;
    }

    pickDate.setDate(pickDate.getDate() + d);

    let result = [];
    data.forEach((d) => {
        if (
            d["Ultah"].getMonth() == pickDate.getMonth() &&
            d["Ultah"].getDate() == pickDate.getDate()
        ) {
            result.push({ Nama: d.Nama, NIM: d.NIM });
        }
    });
    return { Result: result, Date: pickDate };
}
/*
  function test(){
    var e = {
      'parameter': {
        'targetSheet': 'ALL'
      }
    }
  
    if (!e.parameter.targetSheet) {
      Logger.log('error 1')
    }
    var delta = undefined;
    if (e.parameter.delta) {
      delta = e.parameter.delta;
    }
  
    const targetSheet = e.parameter.targetSheet
  
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet()
    if (targetSheet != "ALL") {
      const sheet = spreadsheet.getSheetByName(targetSheet)
      const data = process(sheet, delta)
      Logger.log(JSON.stringify(data))
    } else if (targetSheet == "ALL"){
      var allData = [];
      var date = undefined;
      spreadsheet.getSheets().forEach((s) => {
        objResult = process(s, delta)
        allData = allData.concat(objResult.Result)
        date = objResult.Date
      })
      Logger.log(JSON.stringify({
              'Result': allData,
              'Date': date,
            }))
    }
  }*/
