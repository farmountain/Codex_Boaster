import '../styles/globals.css'
import React from 'react'
import ThemeToggle from '../components/ui/ThemeToggle'
import { ClerkProvider } from '@clerk/nextjs'

const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const content = (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        <div className="p-4 flex justify-end">
          <ThemeToggle />
        </div>
        {children}
      </body>
    </html>
  )

  return publishableKey ? (
    <ClerkProvider publishableKey={publishableKey}>{content}</ClerkProvider>
  ) : (
    content
  )
}
