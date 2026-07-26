import { isAuthenticated } from "./auth.js";

window.location.replace(isAuthenticated() ? "./pages/dashboard.html" : "./pages/login.html");
