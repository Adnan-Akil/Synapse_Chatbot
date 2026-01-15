import { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import { Database, Network } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex h-[100dvh] w-full overflow-hidden bg-zinc-950 text-zinc-100 font-sans selection:bg-teal-500/30">

      {/* Subtle Background Ambience (Alive & Flowing) */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 90, 0],
            opacity: [0.5, 0.8, 0.5],
            x: [0, 100, 0],
            y: [0, -50, 0]
          }}
          transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-[-10%] left-[20%] w-[40%] h-[40%] rounded-full bg-teal-500/20 blur-[100px]"
        />
        <motion.div
          animate={{
            scale: [1, 1.5, 1],
            rotate: [0, -60, 0],
            opacity: [0.4, 0.7, 0.4],
            x: [0, -100, 0],
            y: [0, 100, 0]
          }}
          transition={{ duration: 25, repeat: Infinity, ease: "easeInOut" }}
          className="absolute bottom-[-10%] right-[20%] w-[40%] h-[40%] rounded-full bg-indigo-500/20 blur-[100px]"
        />
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-[40%] left-[40%] w-[20%] h-[20%] rounded-full bg-cyan-500/20 blur-[80px]"
        />
      </div>

      {/* Header / Nav */}
      <header className="absolute top-0 left-0 w-full z-50 p-6 flex justify-between items-center pointer-events-none">

        <div className="flex items-center gap-2 pointer-events-auto">
          <div className="w-8 h-8 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center shadow-lg text-teal-500">
            <Network size={18} />
          </div>
          <span className="font-bold text-zinc-200 tracking-widest text-sm font-mono">SYNAPSE</span>
        </div>

        <div className={`transition-all duration-300 ${isSidebarOpen ? 'opacity-0 pointer-events-none translate-x-10' : 'opacity-100 translate-x-0'}`}>
          <button
            onClick={() => setIsSidebarOpen(true)}
            className="group flex items-center gap-2 px-4 py-2 rounded-full bg-zinc-900/50 backdrop-blur-md border border-zinc-800 hover:border-teal-500/30 text-zinc-400 hover:text-zinc-100 transition-all pointer-events-auto cursor-pointer"
          >
            <span className="text-xs font-medium uppercase tracking-wider">Knowledge Base</span>
            <Database size={14} className="group-hover:text-teal-400 transition-colors" />
          </button>
        </div>
      </header>

      {/* Main Content */}
      {/* Main Content */}
      <div className="relative z-10 flex w-full h-full">
        <ChatWindow isSidebarOpen={isSidebarOpen} />
      </div>

      <Sidebar isOpen={isSidebarOpen} toggleSidebar={() => setIsSidebarOpen(false)} />

    </div>
  );
}

export default App;
