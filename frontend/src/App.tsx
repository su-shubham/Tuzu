import "./App.css";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { Container } from "@mui/system";
import ThemeProvider from "src/ThemeProvider";
import { Helmet, HelmetProvider } from "react-helmet-async";
import { AuthContextProvider } from "./AuthContext";
import { ToastContextProvider } from "./ToastContext";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Router from "./Router";
import Toasts from "./components/Toasts";

function App() {
  return (
    <QueryClientProvider client={new QueryClient()}>
      <AuthContextProvider>
        <HelmetProvider>
          <Helmet>
            <title>Tozo</title>
          </Helmet>
          <ThemeProvider>
            <ToastContextProvider>
              <Container maxWidth="md">
                <Toasts />
                <Router />
              </Container>
            </ToastContextProvider>
          </ThemeProvider>
        </HelmetProvider>
      </AuthContextProvider>
    </QueryClientProvider>
  );
}

export default App;
