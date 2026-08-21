'use client'

import { useState, useRef } from 'react'
import Link from 'next/link'

export default function SourcesManager() {
  const [activeTab, setActiveTab] = useState<'pdf' | 'web' | 'db'>('pdf')
  
  const [isUploading, setIsUploading] = useState(false)
  const [webUrl, setWebUrl] = useState('')
  const [dbString, setDbString] = useState('')
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null)
  
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handlePdfUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return
    const file = e.target.files[0]
    
    setIsUploading(true)
    setMessage(null)
    
    try {
      const formData = new FormData()
      formData.append("file", file)
      
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/sources/pdf`, {
        method: "POST",
        body: formData,
      })
      
      if (res.ok) {
        setMessage({type: 'success', text: `Successfully indexed ${file.name} to Qdrant!`})
      } else {
        setMessage({type: 'error', text: "Failed to upload document."})
      }
    } catch(err) {
      setMessage({type: 'error', text: "Network error connecting to Backend."})
    } finally {
      setIsUploading(false)
    }
  }

  const handleWebSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!webUrl) return
    setIsUploading(true)
    setMessage(null)

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/sources/web`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: webUrl }),
      })
      
      if (res.ok) {
        setMessage({type: 'success', text: `Successfully fetched and indexed ${webUrl} !`})
        setWebUrl('')
      } else {
        setMessage({type: 'error', text: "Failed to fetch URL."})
      }
    } catch(err) {
      setMessage({type: 'error', text: "Network error connecting to Backend."})
    } finally {
      setIsUploading(false)
    }
  }

  const handleDbTest = async (e: React.MouseEvent) => {
    e.preventDefault()
    if (!dbString) return
    setIsUploading(true)
    setMessage(null)
    
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/sources/database`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ connection_string: dbString }),
      })
      
      if (res.ok) {
        setMessage({type: 'success', text: "Successfully validated and bound the MCP Database Agent to your connection string!"})
      } else {
        const errData = await res.json()
        setMessage({type: 'error', text: errData.message || "Failed to test DB connection."})
      }
    } catch(err) {
      setMessage({type: 'error', text: "Network error configuring database."})
    } finally {
      setIsUploading(false)
    }
  }
  
  return (
    <div className="min-h-screen bg-[#070709] text-white p-8">
      <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in duration-500">
        
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-semibold">Manage Evidence Sources</h1>
            <p className="text-white/50 mt-2">Upload documents, register web domains, and configure database connections.</p>
          </div>
          <Link href="/" className="px-4 py-2 border border-white/10 rounded-lg hover:bg-white/5 transition text-sm">
            &larr; Back to Dashboard
          </Link>
        </div>

        {/* Status Notification */}
        {message && (
          <div className={`p-4 rounded-lg font-medium ${message.type === 'success' ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
            {message.text}
          </div>
        )}

        {/* Tab Navigation */}
        <div className="flex space-x-2 border-b border-white/10 pb-px">
          {['pdf', 'web', 'db'].map((tab) => (
            <button
              key={tab}
              onClick={() => { setActiveTab(tab as any); setMessage(null); }}
              className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab 
                  ? 'border-blue-500 text-blue-400' 
                  : 'border-transparent text-white/40 hover:text-white/80'
              }`}
            >
              {tab === 'pdf' && 'PDF Documents'}
              {tab === 'web' && 'Web Sources'}
              {tab === 'db' && 'Database Rules'}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="mt-8 relative">
          <div className="absolute -inset-1 bg-gradient-to-br from-blue-500/10 via-purple-500/5 to-transparent rounded-2xl blur-2xl"></div>
          
          <div className="relative bg-[#111113] border border-white/10 rounded-2xl p-8 shadow-2xl">
            {activeTab === 'pdf' && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <h3 className="text-xl font-medium text-white/90">Upload Local Document</h3>
                  <input type="file" accept=".pdf" className="hidden" ref={fileInputRef} onChange={handlePdfUpload} />
                  <button onClick={() => fileInputRef.current?.click()} disabled={isUploading} className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-lg text-sm transition">
                    Browse Files
                  </button>
                </div>
                <div onClick={() => fileInputRef.current?.click()} className="border-2 border-dashed border-white/10 rounded-xl p-12 text-center text-white/40 hover:border-blue-500/50 hover:text-white/60 transition cursor-pointer">
                  <div className="text-3xl mb-2">{isUploading ? '⏳' : '📄'}</div>
                  <p>{isUploading ? 'Uploading & Indexing to Qdrant...' : 'Drag and drop a PDF file here, or click to browse'}</p>
                  <p className="text-xs mt-2 opacity-50">Limits: 50MB per file. Only readable PDFs allowed.</p>
                </div>
              </div>
            )}

            {activeTab === 'web' && (
              <div className="space-y-6">
                <h3 className="text-xl font-medium text-white/90">Register Web Content</h3>
                <form onSubmit={handleWebSubmit} className="flex space-x-4">
                  <input 
                    type="url" 
                    value={webUrl}
                    onChange={(e) => setWebUrl(e.target.value)}
                    placeholder="https://example.com/press-release" 
                    className="flex-1 bg-black/50 border border-white/10 rounded-lg px-4 py-2 outline-none focus:border-purple-500 transition" 
                    required
                  />
                  <button type="submit" disabled={isUploading} className="px-6 py-2 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 rounded-lg font-medium transition">
                    {isUploading ? 'Indexing...' : 'Fetch & Index'}
                  </button>
                </form>
                <div className="mt-8 border-t border-white/10 pt-6">
                  <p className="text-sm text-white/50 mb-4">You have no web sources indexed yet.</p>
                </div>
              </div>
            )}

            {activeTab === 'db' && (
              <div className="space-y-6">
                <h3 className="text-xl font-medium text-white/90">Connect Relational DB</h3>
                <p className="text-sm text-yellow-500/80 bg-yellow-500/10 p-4 rounded-lg border border-yellow-500/20">
                  ⚠️ The Database MCP operates on read-only permissions exclusively.
                </p>
                <div className="space-y-2">
                  <label className="text-xs text-white/50 uppercase tracking-wider">PostgreSQL Connection String</label>
                  <input type="password" value={dbString} onChange={(e) => setDbString(e.target.value)} placeholder="postgresql://user:password@neon.tech..." className="w-full bg-black/50 border border-white/10 rounded-lg px-4 py-2 outline-none focus:border-green-500" />
                </div>
                <button onClick={handleDbTest} disabled={isUploading || !dbString} className="px-6 py-2 bg-green-600 hover:bg-green-500 disabled:opacity-50 rounded-lg font-medium transition mt-4">
                  {isUploading ? 'Connecting...' : 'Connect & Update MCP'}
                </button>
              </div>
            )}
          </div>
        </div>
        
      </div>
    </div>
  )
}
