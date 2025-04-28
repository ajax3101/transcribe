document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('recentFilesTable');
    if (!table) return;

    $(table).DataTable({
        language: {
            search: "Поиск:",
            paginate: {
                first: "Первая",
                last: "Последняя",
                next: "Следующая",
                previous: "Предыдущая"
            }
        }
    });
});
