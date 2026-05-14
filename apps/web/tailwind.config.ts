import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#18212f",
        steel: "#4f647a",
        mint: "#2f9d7e",
        amber: "#d58936",
        coral: "#d85f55"
      }
    }
  },
  plugins: []
};

export default config;
