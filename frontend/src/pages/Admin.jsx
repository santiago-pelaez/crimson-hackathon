import React, { useState, useEffect } from 'react';
import { Shield, Activity, MapPin, Lock, AlertTriangle, Terminal } from 'lucide-react';

import { Card, CardHeader, CardTitle, CardContent } from '../components/card'; 
import { Button } from '../components/button';
import { Badge } from '../components/badge';

const AdminDashboard = (props) => {
  const isLocked = props.is_locked ?? props.isLocked ?? false;
  const threatLevel = props.threat_level ?? props.threatLevel ?? 0;
  const aiThoughts = props.ai_thoughts ?? props.aiThoughts ?? ["Aegis Intelligence Hub online. How can I assist with your security posture?"];
  const [logs, setLogs] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState([
    { role: 'ai', text: aiThoughts[0] }
  ]);
  const [sending, setSending] = useState(false);

  // get logs from the backnend every time the threat level changes (indicating a new event)
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await fetch('http://localhost:8000/logs');
        const data = await res.json();
        setLogs([...data].reverse()); // Show newest  1st
      } catch (err) {
        console.error("Failed to fetch logs");
      }
    };
    fetchLogs();
  }, [threatLevel]);

  // 2. Handle Gemini Chat
  const handleSendMessage = async () => {
    if (!chatInput.trim() || isLocked || sending) return;
    setSending(true);
    const userMsg = chatInput.trim();
    setChatHistory(prev => [...prev, { role: 'user', text: userMsg }]);
    setChatInput("");

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, context: logs.slice(0, 10) })
      });
      const data = await res.json();
      setChatHistory(prev => [...prev, { role: 'ai', text: data.response }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'ai', text: "Connection error to AI advisor." }]);
      console.error('Chat error', err);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#0B0E14] text-slate-100 p-6 font-sans overflow-hidden">
      
      {/* LOCKDOWN OVERLAY */}
      {isLocked && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center backdrop-blur-2xl bg-black/60 transition-all duration-500">
          <Card className="w-full max-w-lg border-4 border-red-600 bg-[#0B0E14] shadow-[0_0_50px_rgba(220,38,38,0.5)]">
            <CardContent className="pt-10 pb-10 text-center space-y-6">
              <div className="flex justify-center">
                <div className="p-4 bg-red-600/20 rounded-full animate-pulse">
                  <Lock size={64} className="text-red-600" />
                </div>
              </div>
              <h1 className="text-3xl font-black tracking-tighter text-red-600">
                PHYSICAL AUTHENTICATION REQUIRED
              </h1>
              <p className="text-slate-400 font-mono">
                CRITICAL BREACH DETECTED. ALL SYSTEM OPERATIONS FROZEN.
                <br />PLEASE VERIFY ON THE AEGIS HARDWARE DEVICE.
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* STATS ROW */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-[#151921] border-slate-800 shadow-xl">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-xs font-mono uppercase text-slate-500">Threat Meter</CardTitle>
              <AlertTriangle size={16} className={threatLevel > 50 ? "text-red-500" : "text-yellow-500"} />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-black text-cyan-400">{threatLevel}%</div>
              <div className="w-full bg-slate-800 h-2 mt-2 rounded-full overflow-hidden">
                <div 
                  className={`h-full transition-all duration-1000 ${threatLevel > 60 ? 'bg-red-600 shadow-[0_0_10px_red]' : 'bg-cyan-500'}`}
                  style={{ width: `${threatLevel}%` }}
                />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-[#151921] border-slate-800 shadow-xl">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-xs font-mono uppercase text-slate-500">Queue Status</CardTitle>
              <Activity size={16} className="text-cyan-500" />
            </CardHeader>
            <CardContent>
              <Badge variant="outline" className={`text-xl px-4 py-1 font-bold ${
                threatLevel >= 60 ? 'border-red-600 text-red-600' : 
                threatLevel >= 30 ? 'border-yellow-500 text-yellow-500' : 'border-green-500 text-green-500'
              }`}>
                {threatLevel >= 60 ? 'RED' : threatLevel >= 30 ? 'YELLOW' : 'GREEN'}
              </Badge>
            </CardContent>
          </Card>

          <Card className="bg-[#151921] border-slate-800 shadow-xl">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-xs font-mono uppercase text-slate-500">System Health</CardTitle>
              <Shield size={16} className="text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold uppercase">Operational</div>
              <p className="text-xs text-slate-500 font-mono italic">Aegis Core v4.0 Active</p>
            </CardContent>
          </Card>
        </div>

        {/* MIDDLE SECTION */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[400px]">
          <Card className="bg-black border-slate-800 flex flex-col overflow-hidden">
            <CardHeader className="border-b border-slate-800 bg-[#151921]">
              <div className="flex items-center gap-2">
                <Terminal size={14} className="text-cyan-500" />
                <CardTitle className="text-sm font-mono uppercase">Live AI Sentry Monologue</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="flex-1 overflow-y-auto p-4 font-mono text-xs space-y-2 text-cyan-500/80">
              {Array.isArray(aiThoughts) && aiThoughts.length > 0 ? (
                aiThoughts.map((thought, i) => (
                  <div key={i} className="animate-in fade-in slide-in-from-left-2">
                    <span className="text-slate-600">[{new Date().toLocaleTimeString()}]</span> {thought}
                  </div>
                ))
              ) : (
                <div className="animate-pulse">Sentry active. Monitoring network traffic...</div>
              )}
            </CardContent>
          </Card>

          <Card className="bg-[#151921] border-slate-800 relative overflow-hidden flex items-center justify-center">
             <div className="absolute inset-0 opacity-20 pointer-events-none grayscale invert" 
                  style={{ backgroundImage: `url('https://upload.wikimedia.org/wikipedia/commons/e/ec/World_map_blank_without_borders.svg')`, backgroundSize: 'cover' }}>
             </div>
             {threatLevel > 20 && (
                <div className="relative z-10 flex flex-col items-center animate-bounce">
                  <div className="h-4 w-4 bg-red-600 rounded-full shadow-[0_0_15px_red]"></div>
                  <Badge className="bg-red-600 mt-2">THREAT ORIGIN DETECTED</Badge>
                </div>
             )}
             <div className="absolute top-4 left-4 z-20">
                <CardTitle className="text-xs font-mono text-slate-500 flex items-center gap-2">
                  <MapPin size={12}/> GEOFENCE MONITOR
                </CardTitle>
             </div>
          </Card>
        </div>

        {/* BOTTOM SECTION */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="bg-black border-slate-800 lg:col-span-1 overflow-hidden h-[355px]">
            <CardHeader className="bg-[#151921] border-b border-slate-800 py-3">
              <CardTitle className="text-xs font-mono uppercase text-slate-400">Security Events (logs.json)</CardTitle>
            </CardHeader>
            <div className="h-[300px] overflow-y-auto">
              <table className="w-full text-[10px] font-mono text-left">
                <tbody className="divide-y divide-slate-900">
                  {logs.map((log, i) => (
                    <tr key={i} className="hover:bg-white/5 transition-colors">
                      <td className="p-2 text-slate-500 uppercase">{log.status}</td>
                      <td className="p-2 text-cyan-500">{log.username}</td>
                      <td className="p-2 text-right text-slate-600">{log.location || "Unknown"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <Card className="bg-[#151921] border-slate-800 lg:col-span-2 flex flex-col h-[355px]">
            <CardHeader className="py-3">
              <CardTitle className="text-xs font-mono uppercase text-slate-400">Gemini Intelligence Hub</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col gap-4 overflow-hidden">
              <div className="flex-1 overflow-y-auto space-y-4 pr-2 scrollbar-thin scrollbar-thumb-slate-800">
                {chatHistory.map((msg, i) => (
                  <div key={i} className={`flex ${msg.role === 'ai' ? 'justify-start' : 'justify-end'}`}>
                    <div className={`max-w-[80%] rounded-lg px-3 py-2 text-xs font-mono ${
                      msg.role === 'ai' ? 'bg-slate-800 text-cyan-400 border border-cyan-900/30' : 'bg-cyan-600 text-white shadow-lg'
                    }`}>
                      <span className="opacity-50 text-[8px] block mb-1 uppercase font-bold">{msg.role}</span>
                      {msg.text}
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 pt-2 border-t border-slate-800">
                <input 
                    value={chatInput}
                    disabled={isLocked}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                    className={`flex-1 bg-black border border-slate-800 rounded px-4 py-2 text-xs text-white focus:outline-none focus:border-cyan-500 transition-colors ${isLocked ? 'opacity-50 cursor-not-allowed' : ''}`}
                    placeholder={isLocked ? "SYSTEM FROZEN - AUTH REQUIRED" : "Query network intelligence..."}
                  />
                  <Button 
                    onClick={handleSendMessage} 
                    disabled={isLocked}
                    className="bg-cyan-600 hover:bg-cyan-500 h-9 text-xs font-bold transition-all disabled:opacity-50"
                  >
                    Analyze
                  </Button>
              </div>
            </CardContent>
          </Card>
        </div>   
      </div>
    </div>
  );
};

export default AdminDashboard;