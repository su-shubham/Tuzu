import { useMemo } from "react";
import { PaletteMode } from "@mui/material";
import CssBaseline from "@mui/material/CssBaseline";
import useMediaQuery from "@mui/material/useMediaQuery";
import { createTheme, ThemeProvider as MuiThemeProvider } from "@mui/material/styles";

interface IProps {
  children: React.ReactNode;
}

const ThemeProvider = ({ children }: IProps) => {
  const darkMode = useMediaQuery("(prefers-color-scheme:light)")
  const theme = useMemo(() => {
    const palette = {
      mode: (darkMode ? "dark" : "light") as PaletteMode,
    };
    return createTheme({ palette });
  }, [darkMode]);
  return (
    <MuiThemeProvider theme={theme}>
      <CssBaseline enableColorScheme />
      {children}
    </MuiThemeProvider>
  )
}

export default ThemeProvider;