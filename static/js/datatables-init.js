document.addEventListener("DOMContentLoaded", function () {
    const tables = document.querySelectorAll("table");
    if (tables.length > 0 && window.simpleDatatables) {
        tables.forEach((table) => {
            new simpleDatatables.DataTable(table, {
                searchable: false,   // No search
                perPageSelect: false, // No entries per page selector
                paging: false,       // No pagination
                sortable: false,     // Disable sorting
                labels: {            // Remove info text
                    info: ""
                }
            });
        });
    }
});