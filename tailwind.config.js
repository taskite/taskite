/** @type {import('tailwindcss').Config} */
export default {
  content: ['./taskite/static/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#8B5CF6'
      }
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false
  },
}
