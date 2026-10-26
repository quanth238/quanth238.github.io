import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

export type Theme = "light" | "dark";

interface ThemeStore {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set, get) => ({
      theme: "light",
      setTheme: (theme: Theme) => {
        set({ theme });
        updateTheme(theme);
      },
      toggleTheme: () => {
        const theme = get().theme === "dark" ? "light" : "dark";
        set({ theme });
        updateTheme(theme);
      },
    }),
    {
      // The old key may contain the previous automatic system preference.
      // Start this light-first design fresh, then remember explicit choices.
      name: "portfolio-theme-v1",
      merge: (persisted, current) => ({
        ...current,
        theme:
          (persisted as { theme?: unknown } | null)?.theme === "dark"
            ? "dark"
            : "light",
      }),
      storage: createJSONStorage(() => {
        if (typeof window !== "undefined") return localStorage;
        return {
          getItem: () => null,
          setItem: () => {},
          removeItem: () => {},
        };
      }),
    },
  ),
);

function updateTheme(theme: Theme) {
  const root = document.documentElement;
  root.classList.remove("light", "dark");
  root.classList.add(theme);
  root.setAttribute("data-theme", theme);
}
