import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./components/ScrollToTop";
import TopBar from "./components/TopBar";
import Register from "./pages/Register";
import ConfirmEmail from "./pages/ConfirmEmail";

const Router = () => (
    <BrowserRouter>
        <ScrollToTop />
        <TopBar />
        <Routes>
            <Route path="/register/" element={<Register />} />
            {/* Not configured yet */}
            <Route path="/confirm-email/:token/" element={<ConfirmEmail />} />
        </Routes>
    </BrowserRouter>
)

export default Router;