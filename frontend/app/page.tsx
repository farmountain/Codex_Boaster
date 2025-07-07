import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center h-[80vh] space-y-6">
      <h1 className="text-3xl font-bold">Codex Booster</h1>
      <p className="text-center max-w-md">AI-native platform that turns natural language goals into working software using a multi-agent workflow.</p>
      <div className="space-x-4">
        <Link href="/dashboard" className="px-4 py-2 bg-blue-600 text-white rounded">Dashboard</Link>
        <Link href="/signup" className="px-4 py-2 border rounded">Signup</Link>
      </div>
    </main>
  )
}
