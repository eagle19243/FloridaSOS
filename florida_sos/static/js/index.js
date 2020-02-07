var table;
window.onload = () => {
    Init();
}

function Init() {
    table = $('#tbl_corps').DataTable({
        responsive: true,
        fixedHeader: {
            header: true
        },
        fnRowCallback : function(nRow, aData, iDisplayIndex){
            $("td:first", nRow).html(iDisplayIndex +1);
            return nRow;
        },
    })
    $('.btn-refresh').click(() => {
        refreshTable();
    });
    $('.btn-export').click(() => {
        downloadCSV();
    });
    $('.btn-start').click(() => {
        startWorker();
    });
    $('.btn-resume').click(() => {
        resumeWorker();
    });

    refreshTable();
}

function refreshTable() {
    showSpinner();
    table.clear().draw();
    getCorps((corps) => {
        for (var i = 0; i < corps.length; i++) {
            var data = [
                i + 1,
                corps[i].corp_name,
                corps[i].fei_ein_number,
                corps[i].date_filed,
                corps[i].status,
                corps[i].last_event,
                corps[i].principal_addr,
                corps[i].mailing_addr,
                corps[i].registered_agent_addr,
                corps[i].officer_addr,
            ];
            table.row.add(data).draw();
        }
        hideSpinner()
    });
}

function downloadCSV() {
    window.open('/get_csv', '_blank');
}

function getCorps(callback) {
    $.ajax({
        url: '/get_corps',
        method: 'POST',
        success: (result) => {
            callback(JSON.parse(result));
        }
    });
}

function startWorker() {
    $.ajax({
        url: '/restart',
        method: 'POST',
        success: (result) => {
        }
    });
}

function resumeWorker() {
    $.ajax({
        url: '/resume',
        method: 'POST',
        success: (result) => {
        }
    });
}

function showSpinner() {
    $('body').css('overflow', 'hidden');
    $('.spinner-container').show();
}

function hideSpinner() {
    $('body').css('overflow', 'auto');
    $('.spinner-container').hide();
}