import { applyValidationErrors, setButtonLoading, setInlineAlert, showToast } from "./ui.js";
import { getPostAuthRedirect, loginUser, redirectIfAuthenticated } from "./auth.js";
import { initializeThemeToggle } from "./theme.js";
import { qs } from "./utils.js";

async function bootstrap() {
  initializeThemeToggle(document);

  const redirected = await redirectIfAuthenticated("./dashboard.html");
  if (redirected) return;

  const params = new URLSearchParams(window.location.search);
  const authAlert = qs("#auth-alert");
  const initialMessage = params.get("message");

  if (initialMessage) {
    setInlineAlert(authAlert, {
      type: "success",
      message: initialMessage
    });
  }

  const form = qs("#login-form");
  const submitButton = qs("#login-button");

  // SHOW / HIDE PASSWORD
  const passwordInput = document.getElementById("password");
  const passwordToggle = document.getElementById("password-toggle");

  if (passwordInput && passwordToggle) {
    passwordToggle.addEventListener("click", function () {
      if (passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordToggle.textContent = "Hide";
      } else {
        passwordInput.type = "password";
        passwordToggle.textContent = "Show";
      }
    });
  }

  // LOGIN FORM
  form?.addEventListener("submit", async (event) => {
    event.preventDefault();

    applyValidationErrors(form, null);
    setInlineAlert(authAlert, {});

    const formData = new FormData(form);

    const payload = {
      email: String(formData.get("email") || "").trim(),
      password: String(formData.get("password") || "")
    };

    setButtonLoading(submitButton, true, "Signing in…");

    try {
      await loginUser(payload);

      showToast({
        type: "success",
        title: "Welcome back",
        message: "You are now signed in."
      });

      window.location.href = getPostAuthRedirect();

    } catch (error) {
      const applied = applyValidationErrors(form, error);

      setInlineAlert(authAlert, {
        type: "error",
        message: applied
          ? "Please review the highlighted fields."
          : error.message
      });

    } finally {
      setButtonLoading(submitButton, false);
    }
  });
}

bootstrap();
