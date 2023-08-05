import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./components/ScrollToTop";
import TopBar from "./components/TopBar";
import Register from "./pages/Register";
import ConfirmEmail from "./pages/ConfirmEmail";
import Login from "./pages/Login";
import ChangePassword from "./pages/ChangePassword";
import RequireAuth from "./components/RequireAuth";
import ForgotPassword from "src/pages/ForgottenPassword"

const Router = () => (
    <BrowserRouter>
        <ScrollToTop />
        <TopBar />
        <Routes>
            <Route path="/register/" element={<Register />} />
            {/* Not configured yet */}
            <Route path="/confirm-email/:token/" element={<ConfirmEmail />} />
            {/* Not configured yet */}
            <Route path="/login/" element={<Login />} />
            <Route path="/change-password/" element={<RequireAuth><ChangePassword /></RequireAuth>} />
            <Route path="/forgot-password/" element={<ForgotPassword />} />
        </Routes>
    </BrowserRouter>
)

export default Router;