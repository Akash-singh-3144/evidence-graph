'use client'

import React, { useMemo } from 'react';
import ReactFlow, { MiniMap, Controls, Background, useNodesState, useEdgesState, Handle, Position, MarkerType } from 'reactflow';
import 'reactflow/dist/style.css';

// Node configurations based on source type
const sourceStyles: Record<string, any> = {
  database: {
    wrapper: 'hover:bg-emerald-900/40 border-emerald-500/30 hover:shadow-[0_0_30px_rgba(16,185,129,0.3)]',
    gradient: 'from-emerald-500/20 to-teal-500/10',
    badge: 'bg-emerald-500/20 text-emerald-400',
    icon: '💾',
    label: 'Database MCP'
  },
  pdf: {
    wrapper: 'hover:bg-rose-900/40 border-rose-500/30 hover:shadow-[0_0_30px_rgba(244,63,94,0.3)]',
    gradient: 'from-rose-500/20 to-pink-500/10',
    badge: 'bg-rose-500/20 text-rose-400',
    icon: '📄',
    label: 'PDF MCP'
  },
  web: {
    wrapper: 'hover:bg-amber-900/40 border-amber-500/30 hover:shadow-[0_0_30px_rgba(245,158,11,0.3)]',
    gradient: 'from-amber-500/20 to-orange-500/10',
    badge: 'bg-amber-500/20 text-amber-400',
    icon: '🌐',
    label: 'Web MCP'
  },
  query: {
    wrapper: 'hover:bg-blue-900/40 border-blue-500/30 hover:shadow-[0_0_30px_rgba(59,130,246,0.3)]',
    gradient: 'from-blue-500/20 to-indigo-500/10',
    badge: 'bg-blue-500/20 text-blue-400',
    icon: '🔍',
    label: 'Investigation Root'
  }
};

const CustomNode = ({ data, isConnectable }: any) => {
  const type = data.isQuery ? 'query' : (data.detail?.source_type || 'query');
  const style = sourceStyles[type] || sourceStyles.query;

  return (
    <div className={`group relative px-6 py-4 shadow-2xl rounded-2xl bg-[#111113]/80 backdrop-blur-md border ${style.wrapper} overflow-visible min-w-[280px] max-w-[360px] transition-all duration-300`}>
      {/* Node Glow Effect */}
      <div className={`absolute inset-0 bg-gradient-to-br ${style.gradient} rounded-2xl opacity-100 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none`} />
      
      {/* Top Handle */}
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} className="w-3 h-3 bg-white border-2 border-transparent shadow-lg" />
      
      <div className="flex flex-col gap-3 relative z-10">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className={`flex items-center justify-center w-7 h-7 rounded-lg ${style.badge} text-sm shadow-sm`}>
              {style.icon}
            </span>
            <span className="text-[11px] font-bold text-white/70 tracking-wider uppercase">
              {style.label}
            </span>
          </div>
          {data.detail?.score && (
             <span className="text-[10px] bg-white/10 px-2 py-1 rounded text-white/50">{Math.round(data.detail.score*100)}% REL</span>
          )}
        </div>

        <p className="text-sm font-medium text-white/95 leading-relaxed break-words line-clamp-4">
          {data.label}
        </p>

        {data.detail?.claim && data.label !== data.detail.claim && (
          <div className="text-xs text-white/60 bg-black/40 p-2 rounded border border-white/5 italic">
            " {String(data.detail.claim).substring(0, 100)}... "
          </div>
        )}
      </div>

      {/* Bottom Handle */}
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} className="w-3 h-3 bg-white border-2 border-transparent shadow-lg" />
    </div>
  );
};

export default function EvidenceGraph({ graphData }: { graphData?: any }) {
  const nodeTypes = useMemo(() => ({ custom: CustomNode }), []);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  React.useEffect(() => {
    if (graphData && graphData.nodes) {
       const flowNodes = graphData.nodes.map((n: any, i: number) => ({
          id: String(n.id).trim(),
          type: 'custom',
          position: n.position || { x: 50 + (i%3)*400, y: i * 250 },
          data: { 
            label: String(n.data?.label || n.label || n.content || n.id),
            detail: n.data?.detail || null,
            isQuery: String(n.type).toUpperCase() === 'QUERY' 
          },
       }));
       const flowEdges = (graphData.edges || []).map((e: any, i: number) => ({
          id: `e-${i}`,
          source: String(e.source).trim(),
          target: String(e.target).trim(),
          label: (e.label || e.relationship || 'links').toUpperCase(),
          animated: true,
          style: { stroke: '#4b5563', strokeWidth: 2, filter: 'drop-shadow(0 0 2px rgba(255,255,255,0.2))' },
          labelStyle: { fill: '#9ca3af', fontWeight: 600, fontSize: 11, fontFamily: 'monospace' },
          labelBgStyle: { fill: '#0a0a0c', opacity: 0.9 },
          labelBgPadding: [8, 4],
          labelBgBorderRadius: 4,
          markerEnd: { type: MarkerType.ArrowClosed, color: '#4b5563' },
       }));
       if(flowNodes.length > 0) setNodes(flowNodes);
       if(flowEdges.length > 0) setEdges(flowEdges);
    }
  }, [graphData, setNodes, setEdges]);

  return (
    <div className="h-[550px] w-full border border-white/5 rounded-2xl overflow-hidden bg-gradient-to-b from-[#0a0a0c] to-[#111113] shadow-inner relative group">
      <div className="absolute inset-0 bg-[url('https://transparenttextures.com/patterns/cubes.png')] opacity-[0.03] pointer-events-none" />
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        className="font-sans"
      >
        <Controls className="bg-white/5 border-white/10 fill-white drop-shadow-xl" showInteractive={false} />
        <MiniMap nodeStrokeColor="transparent" nodeColor="rgba(255,255,255,0.1)" maskColor="rgba(0,0,0,0.6)" className="bg-transparent border border-white/10 rounded-lg overflow-hidden backdrop-blur-sm" />
        <Background color="#ffffff" gap={24} size={1} className="opacity-[0.04]" />
      </ReactFlow>
    </div>
  );
}
