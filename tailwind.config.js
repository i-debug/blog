// tailwind.config.js
module.exports = {
  content: [
    './templates/**/*.html',
    './blog/**/*.py',
    './core/**/*.py',
    './static/**/*.js',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'apple-blue': '#007AFF',
        'apple-gray': {
          50: '#F2F2F7',
          100: '#E5E5EA',
          200: '#D1D1D6',
          300: '#C7C7CC',
          400: '#AEAEB2',
          500: '#8E8E93',
          600: '#636366',
          700: '#48484A',
          800: '#3A3A3C',
          900: '#1C1C1E'
        },
        'blog-text': '#D1D5DB', // 新增非黑非白的文本颜色
        'blog-bg': '#1F2937'    // 新增深色背景颜色
      },
      fontFamily: {
        'apple': ['-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif']
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.6s ease-out',
        'fade-in': 'fadeIn 0.6s ease-out'
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        }
      }
    }
  },
  plugins: [],
}
