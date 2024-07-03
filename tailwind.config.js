/** @type {import('tailwindcss').Config} */
module.exports = {
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography"), require('flowbite/plugin')],
  content: ["./**/templates/**/*.html", './node_modules/flowbite/**/*.js', 'static/css/styles.css'],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        interest: {
          weak: "#5677CB",
          strong: "#2E68FE"
        },
        quality: {
          weak: "#CBA658",
          strong: "#FFAD00"
        },
        disinterest: {
          weak: "#CB726D",
          strong: "#FE5F57"
        },
        gruv: {
          red: {
            50: "#fb4934",
            100: "#cc241d",
            200: "#9d0006",
          },
          orange: {
            50: "#fe8019",
            100: "#d65d0e",
            200: "#af3a03",
          },
          yellow: {
            50: "#fabd2f",
            100: "#d79921",
            200: "#b57614",
          },
          green: {
            50: "#b8bb26",
            100: "#98971a",
            200: "#79740e",
          },
          aqua: {
            50: "#8ec07c",
            100: "#689d6a",
            200: "#427b58",
          },
          blue: {
            50: "#83a598",
            100: "#458588",
            200: "#076678",
          },
          purple: {
            50: "#d3869b",
            100: "#b16286",
            200: "#8f3f71",
          },
          50: "#fbf1c7",
          100: "#ebdbb2",
          200: "#d5c4a1",
          300: "#bdae93",
          400: "#a89984",
          500: "#7c6f64",
          600: "#665c54",
          700: "#504945",
          800: "#3c3836",
          850: "#32302f",
          900: "#282828",
          950: "#1d2021",

          bg: "#202020",
          light: {
            layer1: "#FAFAFA",
            layer2: "#E0E0E0",
            layer3: "#C0C0C0",
          },
          dark: {
            layer1: "#2A2A2A",
            layer2: "#404040",
            layer3: "#505050"
          },


          fg: "#ebdbb2",
          card: "#3c3836"
        },
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            a: {
              textDecoration: "none",
              "&:hover": {
                textDecoration: "underline",
              },
              "&:visited": {},
            },
          },
        },
      }),
    },
    fontFamily: {
      sans: [
        'Inter',
        'ui-sans-serif',
        'system-ui',
        '-apple-system',
        'system-ui',
        'Segoe UI',
        'Roboto',
        'Helvetica Neue',
        'Arial',
        'Noto Sans',
        'sans-serif',
        'Apple Color Emoji',
        'Segoe UI Emoji',
        'Segoe UI Symbol',
        'Noto Color Emoji'
      ],
      serif: [
        "serif",
        "Apple Color Emoji",
        "Segoe UI Emoji",
        "Segoe UI Symbol",
        "Noto Color Emoji",
      ],
    },
  },
};
