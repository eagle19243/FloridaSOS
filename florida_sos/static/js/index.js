window.onload = () => {
    Init();
}

function Init() {
    var table = $('#tbl_corps').DataTable({
        responsive: true,
        fixedHeader: {
            header: true
        }
    })
    $('.btn-refresh').click(() => {
        window.location.reload();
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
}

function downloadCSV() {
    window.open('/get_csv', '_blank');
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