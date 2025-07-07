'use client'
import { SignUp } from '@clerk/nextjs'
import PlanSelector from '../../../components/PlanSelector'

export default function RegisterPage() {
  return (
    <div className="p-6 space-y-6 flex flex-col items-center">
      <SignUp path="/register" signInUrl="/login" />
      <PlanSelector />
    </div>
  )
}
