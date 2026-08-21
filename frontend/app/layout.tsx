import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'EvidenceGraph - AI Investigation Engine',
  description: 'AI-driven evidence ranking and cross-verification system',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#070709] text-foreground antialiased">
        <header className="border-b border-white/10 p-4">
          <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent max-w-6xl mx-auto">
            EvidenceGraph
          </h1>
        </header>
        {children}
      </body>
    </html>
  )
}
