import type { AppProps } from 'next/app'
import { ClerkProvider } from '@clerk/nextjs'
import '../styles/globals.css'

const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

export default function MyApp({ Component, pageProps }: AppProps) {
  return publishableKey ? (
    <ClerkProvider publishableKey={publishableKey}>
      <Component {...pageProps} />
    </ClerkProvider>
  ) : (
    <Component {...pageProps} />
  );
}
