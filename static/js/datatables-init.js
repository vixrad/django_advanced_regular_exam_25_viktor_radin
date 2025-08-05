document.addEventListener("DOMContentLoaded", function () {
    const tables = document.querySelectorAll("table");
    if (tables.length > 0 && window.simpleDatatables) {
        tables.forEach((table) => {
            new simpleDatatables.DataTable(table);
        });
    }
});