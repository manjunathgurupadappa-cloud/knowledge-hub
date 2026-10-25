/* Knowledge Hub - small progressive enhancements */
document.addEventListener("DOMContentLoaded", function () {
  // 1. Highlight invalid inputs (the server renders the error text).
  document.querySelectorAll(".field-has-error").forEach(function (group) {
    group.querySelectorAll("input, select, textarea").forEach(function (el) {
      el.classList.add("is-invalid");
    });
  });

  // 2. Auto-dismiss success/info messages after 5 seconds.
  document.querySelectorAll(".alert-success, .alert-info").forEach(function (alertEl) {
    setTimeout(function () {
      if (window.bootstrap && document.body.contains(alertEl)) {
        bootstrap.Alert.getOrCreateInstance(alertEl).close();
      }
    }, 5000);
  });

  // 3. Submit filter forms as soon as a dropdown changes.
  document.querySelectorAll("form[data-autosubmit]").forEach(function (form) {
    form.querySelectorAll("[data-autosubmit-field]").forEach(function (field) {
      field.addEventListener("change", function () { form.submit(); });
    });
  });

  // 4. Prevent double submissions of create/edit/delete forms.
  document.querySelectorAll("form[data-prevent-double-submit]").forEach(function (form) {
    form.addEventListener("submit", function () {
      form.querySelectorAll("button[type=submit]").forEach(function (btn) {
        setTimeout(function () { btn.disabled = true; }, 0);
      });
    });
  });
});
