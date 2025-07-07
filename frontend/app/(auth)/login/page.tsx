'use client'
import { SignIn } from '@clerk/nextjs'

export default function LoginPage() {
  return (
    <div className="flex justify-center items-center p-6">
      <SignIn path="/login" signUpUrl="/register" />
    </div>
  )
}
