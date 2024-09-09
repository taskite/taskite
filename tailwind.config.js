/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './ui/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
  corePlugins: {
    preflight: false
  }
}
