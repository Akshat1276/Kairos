/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'kairos-blue': '#1E40AF',
        'kairos-purple': '#7C3AED',
        'kairos-green': '#059669',
        'kairos-red': '#DC2626',
      },
    },
  },
  plugins: [],
};