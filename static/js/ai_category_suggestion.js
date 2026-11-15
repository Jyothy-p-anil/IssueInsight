
document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("ai-suggest-button");
    const result = document.getElementById("ai-suggestion-result");
    const description = document.getElementById("id_description");
    const category = document.getElementById("id_category");
    const form = button?.closest("form");

    if (!button || !result || !description || !category || !form) {
        return;
    }

    const csrfToken = form.querySelector(
        'input[name="csrfmiddlewaretoken"]'
    )?.value;

    const endpoint = button.dataset.url;

    button.addEventListener("click", async function () {
        result.textContent = "";

        if (!description.value.trim()) {
            result.textContent = "Enter a complaint description first.";
            return;
        }

        button.disabled = true;
        button.textContent = "Analyzing...";

        try {
            const body = new URLSearchParams({
                description: description.value
            });

            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: body.toString()
            });

            const data = await response.json();

            if (!response.ok) {
                result.textContent =
                    data.error || "AI suggestion failed.";
                return;
            }

            result.replaceChildren();

            const message = document.createElement("p");
            message.textContent =
                "AI suggests: " + data.category_name +
                (data.needs_review ? " (Review recommended)" : "");
            result.appendChild(message);

            const applyButton = document.createElement("button");
            applyButton.type = "button";
            applyButton.className = "btn btn-sm btn-outline-success";
            applyButton.textContent = "Use Suggested Category";

            applyButton.addEventListener("click", function () {
                category.value = String(data.category_id);
                category.dispatchEvent(
                    new Event("change", { bubbles: true })
                );
                result.textContent =
                    "Selected category: " + data.category_name +
                    ". You can change it before submitting.";
            });

            result.appendChild(applyButton);

        } catch (error) {
            result.textContent =
                "Unable to connect to the AI suggestion service.";
        } finally {
            button.disabled = false;
            button.textContent = "Suggest Category with AI";
        }
    });
});
