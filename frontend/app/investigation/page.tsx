'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import DynamicChart from '@/components/graph/DynamicChart'

export default function InvestigationPage() {
  const searchParams = useSearchParams()
  const query = searchParams.get('query')

  const [loading, setLoading] = useState(true)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!query) return

    const runInvestigation = async () => {
      try {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${API_URL}/api/investigations/query`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query }),
        })
        
        if (!res.ok) throw new Error("Failed to run investigation")
        
        const data = await res.json()
        setResult(data)
      } catch (err: any) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    runInvestigation()
  }, [query])

  if (!query) {
    return <div className="p-8 text-white">No query provided. <Link href="/" className="text-blue-500">Go back.</Link></div>
  }

    const answerRaw = result?.result?.answer || "";
    
    // Intercept Synthetic RAG Graphs generated from unstructured PDFs/Web
    let injectedChart = null;
    const chartMatch = answerRaw.match(/<chart_data>([\s\S]*?)<\/chart_data>/);
    if (chartMatch && chartMatch[1]) {
      try { injectedChart = JSON.parse(chartMatch[1].trim()); } catch(e) {}
    }
    
    const displayAnswer = answerRaw
       .replace(/<chart_data>[\s\S]*?<\/chart_data>/g, "")
       .replace(/Confidence:\s*0\.\d+/ig, '')
       .trim();

    return (
      <div className="min-h-screen bg-[#000000] text-white p-8 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/10 via-[#070709] to-black">
        <div className="max-w-7xl mx-auto space-y-10 animate-in fade-in duration-700 slide-in-from-bottom-8">
          
          {/* Header Section */}
          <div className="flex items-center justify-between border-b border-white/5 pb-6">
            <div className="space-y-2">
              <h1 className="text-4xl font-light tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400">
                Investigation Dashboard
              </h1>
              <p className="text-white/40 text-sm max-w-xl truncate font-mono">
                <span className="text-blue-500/80 mr-2">$ query:</span> 
                "{query}"
              </p>
            </div>
            <Link href="/" className="px-5 py-2.5 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all text-sm font-medium shadow-[0_0_20px_rgba(255,255,255,0.02)] hover:shadow-[0_0_20px_rgba(255,255,255,0.08)]">
              &larr; Back to Control
            </Link>
          </div>
  
          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-500 rounded-xl">
              {error}
            </div>
          )}
  
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <div className="lg:col-span-2 space-y-8">
              <div className="bg-[#111113] border border-white/10 rounded-2xl p-6 shadow-xl space-y-4 relative overflow-hidden group">
                <div className="absolute top-0 left-0 p-4 opacity-5 blur-xl inset-0 bg-gradient-to-br from-green-500/20 to-transparent pointer-events-none" />
                <h3 className="text-xl font-medium text-green-400 relative z-10">Final Conclusion</h3>
                
                {loading ? (
                  <div className="animate-pulse space-y-3 relative z-10">
                    <div className="h-4 bg-white/10 rounded w-3/4"></div>
                    <div className="h-4 bg-white/10 rounded w-full"></div>
                    <div className="h-4 bg-white/10 rounded w-5/6"></div>
                  </div>
                ) : (
                  <div className="text-white/90 text-lg leading-relaxed whitespace-pre-wrap font-light tracking-wide relative z-10 mb-6">
                    {displayAnswer || "The Agent could not determine a definitive answer based on the provided evidence."}
                  </div>
                )}
  
                {/* Renders natively if it parses a quantitative array from Database OR intercepted Synthetic AI tags */}
                <DynamicChart evidenceList={
                  injectedChart 
                    ? [{ source_type: 'database', raw_data_passthrough: { result: injectedChart } }] 
                    : (result?.result?.evidence || [])
                } />
              </div>
            </div>

          <div className="space-y-8">
            <div className="bg-[#111113] border border-white/10 rounded-2xl p-6 shadow-xl text-center">
               <h3 className="text-lg font-medium text-white/50 mb-2">Confidence Score</h3>
               <div className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-br from-blue-400 to-purple-500">
                 {loading ? "..." : (result?.result?.confidence ? `${Math.round(result.result.confidence * 100)}%` : "N/A")}
               </div>
            </div>

            <div className="bg-[#111113] border border-white/10 rounded-2xl p-6 shadow-xl">
              <h3 className="text-lg font-medium text-white/90 mb-4">Live Agent Trace</h3>
              <div className="space-y-4 text-sm font-mono opacity-80 h-[300px] overflow-y-auto">
                <div className="flex space-x-2 text-blue-400"><span>[EVENT]</span><span>Initializing Agentic Flow</span></div>
                <div className="flex space-x-2 text-white/60"><span>[STATE]</span><span>Analyzing Query Constraints</span></div>
                {loading && <div className="flex space-x-2 text-purple-400 animate-pulse"><span>[TOOL]</span><span>Executing MCP Fetch...</span></div>}
                
                {!loading && (
                  <>
                    {result?.result?.tools && result.result.tools.length > 0 && (
                      <div className="flex space-x-2 text-yellow-400"><span>[TOOL]</span><span>Selected Tools: {result.result.tools.join(', ')}</span></div>
                    )}
                    <div className="flex space-x-2 text-green-400"><span>[EVIDENCE]</span><span>Normalized successfully</span></div>
                    <div className="flex space-x-2 text-green-400"><span>[GRAPH]</span><span>Graph generation completed</span></div>
                    <div className="flex space-x-2 text-blue-400"><span>[STATE]</span><span>Synthesis complete</span></div>
                  </>
                )}
              </div>
            </div>

            {/* NEW: Evidence Widget Side Panel */}
            <div className="bg-[#0c0c0e] border border-white/10 rounded-2xl p-6 shadow-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 blur-xl inset-0 bg-gradient-to-bl from-blue-500/20 to-transparent pointer-events-none" />
              <h3 className="text-lg font-medium text-white/90 mb-6 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
                Extracted Evidence
              </h3>
              
              <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                {!loading && result?.result?.evidence?.length === 0 && (
                   <p className="text-white/30 text-sm italic py-4">No structural evidence natively extracted.</p>
                )}
                {!loading && result?.result?.evidence?.map((ev: any, idx: number) => {
                  let badgeColor = 'bg-blue-500/10 text-blue-400 border-blue-500/20';
                  if (ev.source_type === 'database') badgeColor = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
                  if (ev.source_type === 'pdf') badgeColor = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
                  if (ev.source_type === 'web') badgeColor = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
                  
                  return (
                    <div key={idx} className="bg-white/5 border border-white/5 rounded-xl p-4 space-y-3 hover:bg-white/10 transition-colors shadow-sm group/card cursor-pointer">
                      <div className="flex justify-between items-center">
                        <span className={`text-[9px] px-2 py-0.5 border uppercase tracking-widest rounded-md ${badgeColor} font-bold shadow-sm`}>
                          {ev.source_type}
                        </span>
                        {ev.score && <span className="text-[10px] text-white/40 font-mono font-medium">{Math.round(ev.score*100)}% REL</span>}
                      </div>
                      
                      <p className="text-sm text-white/80 leading-relaxed font-light line-clamp-3 group-hover/card:line-clamp-none transition-all">
                        {ev.source_type === 'database' 
                          ? '"Natively executed Dynamic SQL extraction."'
                          : `"${String(ev.content || ev.claim || ev.source_name)}"`
                        }
                      </p>

                      {ev.source_type !== 'database' && ev.citation && (
                        <div className="flex flex-wrap gap-2 text-[9px] font-mono mt-2 pt-2 border-t border-white/10 text-white/40">
                           {ev.citation.url && <span className="bg-white/5 px-2 py-0.5 rounded truncate max-w-[200px]">🌐 {ev.citation.url}</span>}
                           {ev.citation.page && <span className="bg-white/5 px-2 py-0.5 rounded">📄 PG {ev.citation.page}</span>}
                           {ev.source_name && ev.source_name !== 'Unknown' && <span className="bg-white/5 px-2 py-0.5 rounded">📁 {ev.source_name}</span>}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  )
}
