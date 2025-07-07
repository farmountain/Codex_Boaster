import '../styles/globals.css'
import React from 'react'
import ThemeToggle from '../components/ui/ThemeToggle'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        <div className="p-4 flex justify-end"><ThemeToggle /></div>
        {children}
      </body>
    </html>
  )
}
