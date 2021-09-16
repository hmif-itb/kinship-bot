const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();

function getDataFromSheet(sheetsName) {
    var result = [];
    for (const sheetName of sheetsName) {
        const sheet = spreadsheet.getSheetByName(sheetName);
        const data = sheet.getDataRange().getValues();
        const headers = data[0];
        const raw_data = data.slice(1);
        const transformed = [];
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
                transformed.push(object);
            }
        });
        result = result.concat(transformed);
    }
    return result;
}

const MONTHS_NAME = {
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

function fetchData(target) {
    var data = [];
    if (target == "ALL") {
        let sheetsName = [];
        for (const sheet of spreadsheet.getSheets()) {
            sheetsName.push(sheet.getName());
        }
        data = getDataFromSheet(sheetsName);
    } else {
        data = getDataFromSheet(target);
    }
    return data;
}

function getByDate(delta, target) {
    var filterDate = new Date();
    var d;
    if (delta) {
        d = parseInt(delta);
    } else {
        d = 0;
    }
    filterDate.setDate(filterDate.getDate() + d);

    var data = fetchData(target);

    const result = [];
    filterByDate(data, filterDate).forEach((i) => {
        result.push({
            Nama: i.Nama,
            NIM: i.NIM,
            Panggilan: i.Panggilan,
        });
    });
    return {
        Result: result,
        Date: filterDate.getDate() + " " + MONTHS_NAME[filterDate.getMonth()],
    };
}
function getByNIM(nim, target) {
    if (!nim) {
        return {
            errors: "nim is required parameter",
        };
    }

    var data = fetchData(target);

    var result = { errors: "nim is not found" };
    const filtered = filterByNIM(data, nim);
    if (filtered.length !== 0) {
        result = filtered[0];
    }
    return result;
}

function getByPanggilan(panggilan, target) {
    if (!panggilan) {
        return {
            errors: "panggilan is required parameter",
        };
    }

    var data = fetchData(target);

    const result = [];
    filterByPanggilan(data, panggilan).forEach((i) => {
        result.push(i);
    });
    return {
        Result: result,
        Panggilan: panggilan,
    };
}

function filterByDate(data, filterDate) {
    return data.filter(
        (item) =>
            item["Ultah"].getMonth() == filterDate.getMonth() &&
            item["Ultah"].getDate() == filterDate.getDate()
    );
}

function filterByNIM(data, nim) {
    return data.filter((item) => item["NIM"] == nim);
}

function filterByPanggilan(data, panggilan) {
    return data.filter((item) =>
        item["Panggilan"].toLowerCase().indexOf(panggilan) >= 0 ? true : false
    );
}
