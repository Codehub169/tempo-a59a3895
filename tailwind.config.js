/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#007BFF',
        'secondary': '#F8F9FA',
        'accent': '#28A745',
        'text-dark': '#343A40',
        'text-light': '#6C757D',
        'border-color': '#DEE2E6',
        'white-color': '#FFFFFF',
        'success': '#28A745',
        'warning': '#FFC107',
        'error': '#DC3545',
      },
      fontFamily: {
        primary: ['Inter', 'sans-serif'],
        secondary: ['Poppins', 'sans-serif'],
      },
      boxShadow: {
        sm: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      borderRadius: {
        DEFAULT: '8px',
        lg: '12px',
      },
      gridTemplateColumns: {
        'gallery_detail_page_layout': 'repeat(3, 1fr)', // Example: 3 columns for gallery
      },
      gridTemplateRows: {
        'gallery_detail_page_layout_rows': 'repeat(2, auto)', // Example: 2 rows for gallery
      }
    },
  },
  plugins: [],
}
