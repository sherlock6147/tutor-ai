/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./base/**/*.{html,js}","./website/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        'raleway': ["'Raleway'",'sans-serif'],
        'quicksand': ["'Quicksand'",'sans-serif'],
      }
    },
  },
  plugins: [],
}
