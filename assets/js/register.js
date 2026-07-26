import { applyValidationErrors, setButtonLoading, setInlineAlert, showToast } from "./ui.js";
import { getPostAuthRedirect, redirectIfAuthenticated, registerUser } from "./auth.js";
import { initializeThemeToggle } from "./theme.js";
import { qs } from "./utils.js";

function validateBeforeSubmit(payload) {
  if (!payload.username || !payload.email || !payload.password || !payload.confirm_password) {
    return "All fields are required.";
  }
  if (payload.password !== payload.confirm_password) {
    return "Passwords do not match.";
  }
  return "";
}

async function bootstrap() {
  initializeThemeToggle(document);
  const redirected = await redirectIfAuthenticated("./dashboard.html");
  if (redirected) return;

  const form = qs("#register-form");
  const submitButton = qs("#register-button");
  const authAlert = qs("#auth-alert");

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    applyValidationErrors(form, null);
    setInlineAlert(authAlert, {});

    const formData = new FormData(form);
    const payload = {
      username: String(formData.get("username") || "").trim(),
      email: String(formData.get("email") || "").trim(),
      password: String(formData.get("password") || ""),
      confirm_password: String(formData.get("confirm_password") || "")
    };

    const clientError = validateBeforeSubmit(payload);
    if (clientError) {
      setInlineAlert(authAlert, { type: "error", message: clientError });
      return;
    }

    setButtonLoading(submitButton, true, "Creating account…");
    try {
      await registerUser(payload);
      showToast({ type: "success", title: "Account created", message: "Welcome to AlgoLingo." });
      window.location.href = getPostAuthRedirect();
    } catch (error) {
      const applied = applyValidationErrors(form, error);
      setInlineAlert(authAlert, {
        type: "error",
        message: applied ? "Please review the highlighted fields." : error.message
      });
    } finally {
      setButtonLoading(submitButton, false);
    }
  });
}

bootstrap();
