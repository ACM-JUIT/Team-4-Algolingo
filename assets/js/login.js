import {
  applyValidationErrors,
  setButtonLoading,
  setInlineAlert,
  showToast
} from "./ui.js";

import {
  getPostAuthRedirect,
  loginUser,
  redirectIfAuthenticated
} from "./auth.js";

import { initializeThemeToggle } from "./theme.js";
import { qs } from "./utils.js";


async function bootstrap() {

  // Initialize theme toggle
  initializeThemeToggle(document);


  // Redirect already authenticated users
  const redirected = await redirectIfAuthenticated("./dashboard.html");

  if (redirected) return;


  // Get URL parameters
  const params = new URLSearchParams(window.location.search);

  const authAlert = qs("#auth-alert");

  const initialMessage = params.get("message");


  // Show initial message if available
  if (initialMessage) {

    setInlineAlert(authAlert, {
      type: "success",
      message: initialMessage
    });

  }


  // Get login form elements
  const form = qs("#login-form");

  const submitButton = qs("#login-button");


  // Password visibility elements
  const passwordInput = document.getElementById("password");

  const togglePassword = document.getElementById("toggle-password");


  // Password Show / Hide functionality
  if (passwordInput && togglePassword) {

    togglePassword.addEventListener("click", () => {

      const isPasswordHidden =
        passwordInput.type === "password";


      if (isPasswordHidden) {

        passwordInput.type = "text";

        togglePassword.textContent = "Hide";

      } else {

        passwordInput.type = "password";

        togglePassword.textContent = "Show";

      }


      // Update accessibility label
      togglePassword.setAttribute(
        "aria-label",
        passwordInput.type === "password"
          ? "Show password"
          : "Hide password"
      );

    });

  }


  // Login form submission
  form?.addEventListener("submit", async (event) => {

    event.preventDefault();


    // Clear previous validation errors
    applyValidationErrors(form, null);

    setInlineAlert(authAlert, {});


    // Get form data
    const formData = new FormData(form);


    // Create login payload
    const payload = {

      email: String(
        formData.get("email") || ""
      ).trim(),

      password: String(
        formData.get("password") || ""
      )

    };


    // Show loading state
    setButtonLoading(
      submitButton,
      true,
      "Signing in…"
    );


    try {

      // Login user
      await loginUser(payload);


      // Show success message
      showToast({
        type: "success",
        title: "Welcome back",
        message: "You are now signed in."
      });


      // Redirect after successful login
      window.location.href =
        getPostAuthRedirect();


    } catch (error) {

      // Apply validation errors
      const applied =
        applyValidationErrors(
          form,
          error
        );


      // Show error message
      setInlineAlert(authAlert, {

        type: "error",

        message: applied
          ? "Please review the highlighted fields."
          : error.message

      });


    } finally {

      // Remove loading state
      setButtonLoading(
        submitButton,
        false
      );

    }

  });

}


// Start login page
bootstrap();