// tailwind.config.js
module.exports = {
  content: [
    '../../templates/**/*.html',
    '../../blog/**/*.py',
    '../../core/**/*.py',
    '../../static/**/*.js',
  ],
  safelist: [
    // 生成所有自定义颜色的类
    { pattern: /bg-(apple-blue|apple-gray|blog-text|blog-bg)/ },
    { pattern: /text-(apple-blue|apple-gray|blog-text|blog-bg)/ },
    { pattern: /border-(apple-blue|apple-gray|blog-text|blog-bg)/ },
    // 生成所有动画类
    { pattern: /animate-(fade-in-up|fade-in)/ },
    // 生成所有字体类
    { pattern: /font-apple/ },
    // 生成常用的工具类
    'container', 'mx-auto', 'px-4', 'py-8', 'text-center', 'bg-gray-800', 'text-white',
    'rounded', 'shadow', 'hover:shadow-lg', 'transition', 'duration-300',
    // 生成所有可能用到的颜色变体
    'bg-apple-gray-50', 'bg-apple-gray-100', 'bg-apple-gray-200', 'bg-apple-gray-300', 'bg-apple-gray-400',
    'bg-apple-gray-500', 'bg-apple-gray-600', 'bg-apple-gray-700', 'bg-apple-gray-800', 'bg-apple-gray-900',
    'text-apple-gray-50', 'text-apple-gray-100', 'text-apple-gray-200', 'text-apple-gray-300', 'text-apple-gray-400',
    'text-apple-gray-500', 'text-apple-gray-600', 'text-apple-gray-700', 'text-apple-gray-800', 'text-apple-gray-900',
    'bg-apple-blue', 'text-apple-blue', 'bg-blog-text', 'text-blog-text', 'bg-blog-bg', 'text-blog-bg',
    'animate-fade-in-up', 'animate-fade-in', 'font-apple',
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
        'blog-text': '#D1D5DB',
        'blog-bg': '#1F2937'
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
