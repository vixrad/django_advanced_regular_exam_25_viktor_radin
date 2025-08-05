document.addEventListener("DOMContentLoaded", function () {
    const ownerToggle = document.getElementById("owner-toggle");
    const userToggle = document.getElementById("user-toggle");
    const companyField = document.getElementById("company-number-field");
    const isOwnerInput = document.getElementById("id_is_owner");
    const companyNumberInput = document.getElementById("id_company_number");
    const companyNameField = document.getElementById("company-name-field");
    const companyAddressField = document.getElementById("company-address-field");

    const API_BASE = "/accounts/api/companies/";
    const INVALID_MESSAGE = "Add a valid company number";
    const DEFAULT_MESSAGE = "Automatically populated";

    function showOwnerFields(show) {
        companyField.style.display = show ? "block" : "none";
        if (!show) {
            companyNameField.value = "";
            companyAddressField.value = "";
        }
    }

    async function fetchCompanyDetails(companyNumber) {
        if (!companyNumber || !/^[A-Za-z0-9]+$/.test(companyNumber)) {
            companyNameField.value = INVALID_MESSAGE;
            companyAddressField.value = INVALID_MESSAGE;
            return;
        }

        companyNameField.value = "Loading...";
        companyAddressField.value = "Loading...";

        try {
            const response = await fetch(`${API_BASE}${companyNumber}/`);
            const data = await response.json();

            if (response.ok && data.company_name) {
                companyNameField.value = data.company_name;
                companyAddressField.value = data.registered_office_address || INVALID_MESSAGE;
            } else {
                companyNameField.value = INVALID_MESSAGE;
                companyAddressField.value = INVALID_MESSAGE;
            }
        } catch (error) {
            companyNameField.value = INVALID_MESSAGE;
            companyAddressField.value = INVALID_MESSAGE;
        }
    }

    companyNumberInput?.addEventListener("blur", function () {
        const companyNumber = this.value.trim();
        fetchCompanyDetails(companyNumber);
    });

    ownerToggle.addEventListener("change", function () {
        isOwnerInput.value = "True";
        showOwnerFields(true);
        companyNameField.value = DEFAULT_MESSAGE;
        companyAddressField.value = DEFAULT_MESSAGE;
    });

    userToggle.addEventListener("change", function () {
        isOwnerInput.value = "False";
        showOwnerFields(false);
    });

    // Default state
    companyNameField.value = DEFAULT_MESSAGE;
    companyAddressField.value = DEFAULT_MESSAGE;
    showOwnerFields(false);
});