// API utility methods
const API_BASE = process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}/api` : "http://localhost:8000/api"

export const api = {
    async queryInvestigation(query: string) {
        const response = await fetch(`${API_BASE}/investigations/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        })
        if (!response.ok) throw new Error("Failed to start investigation")
        return response.json()
    },
    
    async getSources() {
        const response = await fetch(`${API_BASE}/sources`)
        if (!response.ok) throw new Error("Failed to fetch sources")
        return response.json()
    }
}
