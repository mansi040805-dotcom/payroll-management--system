/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        mint: {
          50: '#F0FBF5',
          100: '#E1F7EC',
          200: '#C7EEDD',
          300: '#9DDFC0',
          400: '#B7E7B2',
          500: '#54C7C1',
          600: '#168C87',
          700: '#0F6B67',
        },
        navy: {
          900: '#17153D',
          800: '#22204B',
          700: '#2F2B61',
          600: '#45407D',
          500: '#645F9E',
          400: '#8E8AB8',
          300: '#B5B2D4',
        },
        tealbrand: {
          DEFAULT: '#168C87',
          light: '#77D4C7',
          dark: '#0E5C59',
        },
        accentpurple: {
          DEFAULT: '#8D72DF',
          deep: '#5C3EBA',
          light: '#B4A2F3',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'mockup': '0 30px 80px -15px rgba(23, 21, 61, 0.18), 0 15px 35px -10px rgba(22, 140, 135, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.8) inset',
        'subtle': '0 10px 30px -5px rgba(23, 21, 61, 0.06)',
        'squircle': '0 12px 28px -6px rgba(23, 21, 61, 0.1), 0 2px 8px -2px rgba(23, 21, 61, 0.04)',
        'glow': '0 0 40px rgba(119, 212, 199, 0.35)',
      }
    },
  },
  plugins: [],
}
