import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <h1>Codex Booster</h1>
      <p>AI-native platform for building software.</p>
      <nav>
        <Link href="/about">About</Link> |{' '}
        <Link href="/pricing">Pricing</Link> |{' '}
        <Link href="/dashboard">Dashboard</Link> |{' '}
        <Link href="/contact">Contact</Link>
      </nav>
    </div>
  );
}
