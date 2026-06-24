"use client";

import React, { useState } from "react";
import axios from "axios";
import { ArrowRight, CheckCircle2, Code2, Database, Layout, Loader2, PlayCircle, ShieldCheck, Zap } from "lucide-react";

const BACKEND_URL = "http://localhost:8000";

const STAGES = [
  { id: "intent", label: "Intent Extraction", icon: Zap },
  { id: "architecture", label: "System Design", icon: Layout },
  { id: "schema", label: "DB Schema Generation", icon: Database },
  { id: "api", label: "API Specification", icon: Code2 },
  { id: "ui", label: "UI Generation", icon: Layout },
  { id: "auth", label: "Auth Rules", icon: ShieldCheck },
];

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [output, setOutput] = useState<any>(null);
  const [activeStage, setActiveStage] = useState<number>(-1);
  const [error, setError] = useState<string | null>(null);
  const [executionResult, setExecutionResult] = useState<any>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setIsLoading(true);
    setError(null);
    setOutput(null);
    setExecutionResult(null);
    setActiveStage(0);

    // Simulate stage progression for visual effect (since the backend executes as a single call)
    const stageInterval = setInterval(() => {
      setActiveStage((prev) => {
        if (prev >= STAGES.length - 1) {
          clearInterval(stageInterval);
          return prev;
        }
        return prev + 1;
      });
    }, 800);

    try {
      const response = await axios.post(`${BACKEND_URL}/generate`, { prompt });
      setOutput(response.data);
      setActiveStage(STAGES.length);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "An error occurred");
      setActiveStage(-1);
    } finally {
      setIsLoading(false);
      clearInterval(stageInterval);
    }
  };

  const handleExecute = async () => {
    if (!output) return;
    setIsLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/execute`, { schema_data: output });
      setExecutionResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white font-sans selection:bg-purple-500/30">
      {/* Background gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-purple-600/20 blur-[120px] rounded-full mix-blend-screen" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-blue-600/20 blur-[120px] rounded-full mix-blend-screen" />
      </div>

      <main className="relative z-10 max-w-6xl mx-auto px-6 py-20 flex flex-col gap-12">
        <header className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm font-medium text-purple-300 mb-4">
            <Zap size={14} />
            AI Compiler Engine
          </div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-white/90 to-white/50">
            Natural Language to <br className="hidden md:block" /> Executable Software
          </h1>
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
            Input open-ended instructions. The multi-stage compiler extracts intent, designs the architecture, enforces strict schemas, repairs logic errors, and outputs a runtime-ready application.
          </p>
        </header>

        <section className="w-full max-w-3xl mx-auto flex flex-col gap-4">
          <div className="relative group">
            <textarea
              className="w-full h-32 bg-white/5 border border-white/10 rounded-2xl p-6 text-lg text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all resize-none shadow-2xl backdrop-blur-sm"
              placeholder="e.g. Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <button
              onClick={handleGenerate}
              disabled={isLoading || !prompt.trim()}
              className="absolute bottom-4 right-4 bg-white text-black px-6 py-2.5 rounded-xl font-semibold hover:bg-neutral-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg"
            >
              {isLoading ? <Loader2 className="animate-spin" size={18} /> : <ArrowRight size={18} />}
              Compile
            </button>
          </div>
          {error && <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl">{error}</div>}
        </section>

        {(activeStage >= 0 || output) && (
          <section className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Pipeline Visualizer */}
            <div className="lg:col-span-4 flex flex-col gap-4">
              <h3 className="text-xl font-semibold text-white/90">Compilation Pipeline</h3>
              <div className="bg-white/5 border border-white/10 rounded-2xl p-6 flex flex-col gap-6 backdrop-blur-md">
                {STAGES.map((stage, idx) => {
                  const Icon = stage.icon;
                  const isActive = activeStage === idx;
                  const isCompleted = activeStage > idx || output !== null;
                  
                  return (
                    <div key={stage.id} className={`flex items-center gap-4 transition-all duration-500 ${isCompleted ? 'opacity-100' : isActive ? 'opacity-100 translate-x-2' : 'opacity-30'}`}>
                      <div className={`p-2 rounded-lg ${isCompleted ? 'bg-purple-500/20 text-purple-400' : isActive ? 'bg-blue-500/20 text-blue-400 animate-pulse' : 'bg-white/5 text-white/50'}`}>
                        {isCompleted ? <CheckCircle2 size={20} /> : <Icon size={20} />}
                      </div>
                      <span className={`font-medium ${isCompleted ? 'text-white' : isActive ? 'text-blue-200' : 'text-neutral-500'}`}>
                        {stage.label}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Output Viewer */}
            <div className="lg:col-span-8 flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-semibold text-white/90">Compiled Schema Output</h3>
                {output && (
                  <button onClick={handleExecute} disabled={isLoading} className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 shadow-[0_0_20px_rgba(168,85,247,0.4)]">
                    <PlayCircle size={18} />
                    Simulate Runtime
                  </button>
                )}
              </div>
              <div className="bg-[#111] border border-white/10 rounded-2xl p-6 h-[500px] overflow-auto custom-scrollbar relative">
                {output ? (
                  <pre className="text-sm text-green-400 font-mono">
                    {JSON.stringify(output, null, 2)}
                  </pre>
                ) : (
                  <div className="absolute inset-0 flex items-center justify-center text-neutral-600 font-mono text-sm">
                    {isLoading ? "Awaiting compiler completion..." : "No output generated yet."}
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {/* Runtime Execution Results */}
        {executionResult && (
          <section className="bg-white/5 border border-white/10 rounded-2xl p-8 backdrop-blur-md animate-in slide-in-from-bottom-4 duration-500">
            <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
              <Database className="text-purple-400" />
              Runtime Simulation Success
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-black/40 rounded-xl p-4 border border-white/5">
                <div className="text-neutral-400 text-sm mb-1">Status</div>
                <div className="text-green-400 font-medium font-mono">{executionResult.status}</div>
              </div>
              <div className="bg-black/40 rounded-xl p-4 border border-white/5 md:col-span-2">
                <div className="text-neutral-400 text-sm mb-1">Message</div>
                <div className="text-white font-medium">{executionResult.message}</div>
              </div>
              <div className="bg-black/40 rounded-xl p-4 border border-white/5">
                <div className="text-neutral-400 text-sm mb-2">Tables Created</div>
                <div className="flex flex-wrap gap-2">
                  {executionResult.tables_created?.map((t: string) => (
                    <span key={t} className="px-2 py-1 bg-white/10 rounded text-xs font-mono">{t}</span>
                  ))}
                </div>
              </div>
               <div className="bg-black/40 rounded-xl p-4 border border-white/5 md:col-span-2">
                <div className="text-neutral-400 text-sm mb-2">Simulated Endpoints</div>
                <div className="flex flex-col gap-2">
                  {executionResult.api_endpoints_simulated?.map((t: string) => (
                    <span key={t} className="px-2 py-1 bg-white/5 border border-white/10 rounded text-xs font-mono text-blue-300">{t}</span>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
