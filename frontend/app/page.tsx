'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export default function Home() {
  const [query, setQuery] = useState('')
  const router = useRouter()

  const handleInvestigate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return
    router.push(`/investigation?query=${encodeURIComponent(query)}`)
  }

  return (
    <div className="h-full flex flex-col p-8 space-y-8 animate-in fade-in duration-500">
      <div className="max-w-3xl mx-auto w-full space-y-4">
        <h2 className="text-3xl font-semibold">Start an Investigation</h2>
        <p className="text-white/60">Cross-verify uploaded documents, database tables, and live web sources.</p>
        
        <form onSubmit={handleInvestigate} className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-xl blur opacity-30 group-hover:opacity-50 transition duration-1000"></div>
          <div className="relative flex items-center bg-[#111113] rounded-xl p-2 border border-white/10">
            <input 
              type="text" 
              className="flex-1 bg-transparent px-4 py-2 outline-none placeholder:text-white/30"
              placeholder="E.g., Why did our Q2 revenue decrease?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              required
            />
            <button className="px-6 py-2 bg-blue-600 hover:bg-blue-500 transition-colors rounded-lg font-medium">
              Investigate
            </button>
          </div>
        </form>
      </div>
      
    {/* Dashboard stubs */}
      <h3 className="max-w-5xl mx-auto w-full text-xl font-medium mt-12 mb-[-1rem]">Manage Sources</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto w-full mt-12">
        <Link href="/sources" className="p-6 rounded-2xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-colors cursor-pointer flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-lg mb-2 text-blue-400">PDF Documents</h3>
            <p className="text-sm text-white/50">Manage uploaded files and internal reports.</p>
          </div>
          <div className="mt-4 text-blue-400/80 text-sm font-medium flex items-center">
            Upload PDFs &rarr;
          </div>
        </Link>
        <Link href="/sources" className="p-6 rounded-2xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-colors cursor-pointer flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-lg mb-2 text-green-400">Database Sources</h3>
            <p className="text-sm text-white/50">Browse connected Postgres SQL schemas.</p>
          </div>
          <div className="mt-4 text-green-400/80 text-sm font-medium flex items-center">
            Connect Databases &rarr;
          </div>
        </Link>
        <Link href="/sources" className="p-6 rounded-2xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-colors cursor-pointer flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-lg mb-2 text-purple-400">Web Search</h3>
            <p className="text-sm text-white/50">Configure allowed URLs and live web querying.</p>
          </div>
          <div className="mt-4 text-purple-400/80 text-sm font-medium flex items-center">
            Add URLs &rarr;
          </div>
        </Link>
      </div>
    </div>
  )
}
