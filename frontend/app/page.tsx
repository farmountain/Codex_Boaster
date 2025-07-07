import Link from 'next/link'
import tokens from '../styles/tokens.json'

type Feature = {
  title: string
  description: string
  href: string
}

const { colors } = tokens as { colors: Record<string, string> }

const features: Feature[] = [
  {
    title: 'Agent Dashboard',
    description: 'Run multi-agent workflows',
    href: '/dashboard',
  },
  {
    title: 'Prompt Editor',
    description: 'Craft and test prompts',
    href: '/prompt-editor',
  },
  {
    title: 'Analytics',
    description: 'Inspect performance metrics',
    href: '/analytics',
  },
]

export default function HomePage() {
  return (
    <main className="flex flex-col">
      <section
        className="text-center py-20 px-4"
        style={{
          background: `linear-gradient(90deg, ${colors.primary}, ${colors.secondary})`,
          color: colors.background,
        }}
      >
        <h1 className="text-4xl font-bold mb-4">Codex Booster</h1>
        <p className="max-w-xl mx-auto mb-8">
          AI-native platform that turns natural language goals into working
          software using a multi-agent workflow.
        </p>
        <Link
          href="/dashboard"
          className="inline-block px-6 py-3 rounded font-semibold"
          style={{ backgroundColor: colors.accent, color: '#fff' }}
        >
          Get Started
        </Link>
      </section>

      <section className="max-w-5xl mx-auto grid gap-6 py-12 px-4 sm:grid-cols-2 md:grid-cols-3">
        {features.map((f) => (
          <Link
            key={f.title}
            href={f.href}
            className="p-6 rounded border shadow-sm hover:shadow transition bg-white dark:bg-gray-800"
          >
            <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {f.description}
            </p>
          </Link>
        ))}
      </section>
    </main>
  )
}
