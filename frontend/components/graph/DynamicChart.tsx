'use client'

import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, AreaChart, Area } from 'recharts';

export default function DynamicChart({ evidenceList }: { evidenceList: any[] }) {
  // Deep parse RAG text blobs to find valid JSON numerical arrays from Database execution
  const chartData = useMemo(() => {
    if (!evidenceList || !Array.isArray(evidenceList)) return null;
    
    // First, strictly try to plot Database numerical Arrays
    for (const ev of evidenceList) {
      if (ev.source_type === 'database' && ev.raw_data_passthrough?.result) {
         let parsed = ev.raw_data_passthrough.result;
         if (typeof parsed === 'string') {
             try { parsed = JSON.parse(parsed); } catch(e) {}
         }
         if (Array.isArray(parsed) && parsed.length > 0) {
           const keys = Object.keys(parsed[0]);
           if (keys.length > 0) {
             return { data: parsed, keys, type: 'area', title: 'Database Extracted Analytics', subtitle: 'Live SQL Execution Chart Payload', color: '#10b981' };
           }
         }
      }
    }
    
    return null;
  }, [evidenceList]);

  if (!chartData) {
    return null; // Return absolutely nothing if there is no mathematical tabular array
  }

  const { data, keys, type, title, subtitle, color } = chartData;
  const xAxisKey = keys[0];
  const dataKeys = keys.slice(1).length > 0 ? keys.slice(1) : [keys[0]];

  return (
    <div className="h-[400px] w-full border border-blue-500/20 rounded-2xl overflow-hidden bg-gradient-to-br from-[#0c0c0e] via-[#111113] to-[#070709] shadow-[0_10px_40px_rgba(59,130,246,0.1)] p-6 relative group transition-all hover:border-blue-500/40">
      <div className={`absolute top-0 right-0 p-8 opacity-20 blur-3xl inset-0 bg-gradient-to-l pointer-events-none`} style={{ backgroundColor: color }} />
      <div className="absolute inset-0 bg-[url('https://transparenttextures.com/patterns/cubes.png')] opacity-[0.02]" />
      
      <div className="flex items-center gap-3 mb-6 relative z-10">
        <span className="flex items-center justify-center w-8 h-8 rounded-lg border shadow-lg" style={{ color: color, borderColor: `${color}40`, backgroundColor: `${color}15` }}>
           {type === 'area' ? '📈' : '📊'}
        </span>
        <div>
          <h3 className="font-semibold text-sm text-white/90 uppercase tracking-widest">{title}</h3>
          <p className="text-[10px] text-white/40 font-mono">{subtitle}</p>
        </div>
      </div>

      <ResponsiveContainer width="100%" height="80%">
        {type === 'area' ? (
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorMetric" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={color} stopOpacity={0.6}/>
                <stop offset="95%" stopColor={color} stopOpacity={0}/>
              </linearGradient>
              <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                 <feGaussianBlur stdDeviation="3" result="blur" />
                 <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>
            <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis dataKey={xAxisKey} stroke="#444" tick={{ fill: '#777', fontSize: 11, fontFamily: 'monospace' }} tickMargin={10} />
            <YAxis stroke="#444" tick={{ fill: '#777', fontSize: 11, fontFamily: 'monospace' }} tickMargin={10} width={45} />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(12,12,14,0.95)', border: `1px solid ${color}40`, borderRadius: '12px', color: '#fff', backdropFilter: 'blur(10px)', boxShadow: '0 10px 25px rgba(0,0,0,0.5)' }} 
              itemStyle={{ color: color, fontWeight: 600 }}
              cursor={{ fill: 'rgba(255,255,255,0.02)' }}
            />
            {dataKeys.map((key, idx) => (
               <Area 
                  key={idx} type="monotone" dataKey={key} stroke={color} fillOpacity={1} fill="url(#colorMetric)" strokeWidth={3}
                  activeDot={{ r: 6, fill: color, stroke: '#fff', strokeWidth: 2, filter: 'url(#glow)' }}
               />
            ))}
          </AreaChart>
        ) : (
          <BarChart data={data} barSize={40}>
            <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis dataKey={xAxisKey} stroke="#444" tick={{ fill: '#777', fontSize: 11, fontFamily: 'monospace' }} tickMargin={10} />
            <YAxis stroke="#444" tick={{ fill: '#777', fontSize: 11, fontFamily: 'monospace' }} tickMargin={10} width={45} />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(12,12,14,0.95)', border: `1px solid ${color}40`, borderRadius: '12px', color: '#fff', backdropFilter: 'blur(10px)', boxShadow: '0 10px 25px rgba(0,0,0,0.5)' }} 
              itemStyle={{ color: color, cursor: 'pointer', fontWeight: 600 }}
              cursor={{ fill: 'rgba(255,255,255,0.05)' }}
            />
            {dataKeys.map((key, idx) => (
               <Bar key={idx} dataKey={key} fill={color} radius={[4, 4, 0, 0]} fillOpacity={0.8} />
            ))}
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
