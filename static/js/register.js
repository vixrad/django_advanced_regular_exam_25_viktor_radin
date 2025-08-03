document.addEventListener("DOMContentLoaded", function () {
    const ownerToggle = document.getElementById("owner-toggle");
    const userToggle = document.getElementById("user-toggle");
    const companyField = document.getElementById("company-number-field");
    const isOwnerInput = document.getElementById("id_is_owner");
    const companyNumberInput = document.getElementById("id_company_number");

    const companyNameField = document.getElementById("company-name-field");
    const companyAddressField = document.getElementById("company-address-field");

    function updateForm() {
        if (ownerToggle.checked) {
            companyField.style.display = "block";
            isOwnerInput.value = "True";
        } else {
            companyField.style.display = "none";
            isOwnerInput.value = "False";

            // Clear company info
            companyNameField.value = "";
            companyAddressField.value = "";
        }
    }

    async function fetchCompanyDetails(companyNumber) {
        if (!companyNumber) return;

        try {
            const response = await fetch(`/accounts/api/companies/${companyNumber}/`);
            const data = await response.json();

            if (response.ok) {
                companyNameField.value = data.company_name || "";
                companyAddressField.value = data.registered_office_address || "";
            } else {
                companyNameField.value = "Not found";
                companyAddressField.value = "";
            }
        } catch (error) {
            console.error("Error fetching company details:", error);
        }
    }

    companyNumberInput?.addEventListener("blur", function () {
        const companyNumber = this.value.trim();
        if (companyNumber) fetchCompanyDetails(companyNumber);
    });

    ownerToggle.addEventListener("change", updateForm);
    userToggle.addEventListener("change", updateForm);

    updateForm();
});