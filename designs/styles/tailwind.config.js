/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../../apps/**/*.{html,js,ts,jsx,tsx,py}",
    "./components/**/*.{html,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#06b6d4",
        secondary: "#3b82f6",
        background: "#0f172a",
        surface: "#1e293b"
      }
    }
  },
  plugins: []
};
