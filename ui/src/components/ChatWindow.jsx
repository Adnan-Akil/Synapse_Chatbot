import { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, ArrowUp } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';
import clsx from 'clsx';
import ReactMarkdown from 'react-markdown';


const ChatWindow = () => {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]); // Start empty to show Hero
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    const handleSend = async (text = input) => {
        if (!text.trim()) return;

        const userMessage = text;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await axios.post('http://localhost:8000/chat', {
                message: userMessage,
                history: [] // Simplified for now
            });
            const aiMessage = response.data.response;
            setMessages(prev => [...prev, { role: 'assistant', content: aiMessage }]);
        } catch {
            setMessages(prev => [...prev, { role: 'assistant', content: "Unable to connect to the brain." }]);
        } finally {
            setIsLoading(false);
            // Keep focus
            setTimeout(() => inputRef.current?.focus(), 100);
        }
    };

    return (
        <main className="flex-1 flex flex-col h-full relative max-w-5xl mx-auto w-full">

            {/* Scroll Area */}
            <div className="flex-1 overflow-y-auto w-full scroll-smooth pt-24 pb-32 px-4 no-scrollbar">

                {/* Hero State (Empty) */}
                {messages.length === 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="h-full flex flex-col items-center justify-center text-center space-y-8 pb-20"
                    >
                        <div className="space-y-4 max-w-lg">
                            <h1 className="text-4xl md:text-5xl font-light tracking-tight text-transparent bg-clip-text bg-gradient-to-b from-zinc-100 to-zinc-500">
                                How can I help?
                            </h1>
                            <p className="text-zinc-500 text-lg font-light">
                                Upload documents to give me context, then ask away.
                            </p>
                        </div>

                        {/* Suggestions */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl px-6">
                            {["Summarize this document", "What are the key findings?", "Explain the methodology", "Draft an email based on this"].map((q) => (
                                <button
                                    key={q}
                                    onClick={() => handleSend(q)}
                                    className="p-4 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-900/30 hover:bg-zinc-900/50 text-left text-zinc-400 hover:text-zinc-200 transition-all text-sm"
                                >
                                    {q}
                                </button>
                            ))}
                        </div>
                    </motion.div>
                )}

                {/* Messages */}
                <div className="space-y-8">
                    {messages.map((msg, idx) => (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            key={idx}
                            className={clsx(
                                "flex flex-col gap-2 max-w-3xl mx-auto",
                                msg.role === 'user' ? "items-end" : "items-start"
                            )}
                        >
                            {/* Role Label (Minimal) */}
                            <span className="text-[10px] font-bold tracking-widest text-zinc-600 uppercase mb-1 ml-1">
                                {msg.role === 'assistant' ? 'Synapse' : 'You'}
                            </span>

                            {/* Content */}
                            <div className={clsx(
                                "px-6 py-4 rounded-2xl text-[15px] leading-7 md:text-base",
                                msg.role === 'assistant'
                                    ? "bg-transparent text-zinc-300 -ml-6" // Minimal "No bubble" look for AI
                                    : "bg-zinc-800 text-zinc-100 rounded-br-sm" // Subtle bubble for user
                            )}>
                                <div className="prose prose-invert prose-p:leading-relaxed prose-pre:bg-zinc-900 prose-pre:border prose-pre:border-zinc-800">
                                    <ReactMarkdown>
                                        {String(msg.content || '')}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        </motion.div>
                    ))}

                    {isLoading && (
                        <div className="max-w-3xl mx-auto flex items-center gap-3 text-zinc-500">
                            <Sparkles size={16} className="animate-pulse" />
                            <span className="text-xs tracking-wider">THINKING</span>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area (Floating Pill) */}
            <div className="absolute bottom-0 left-0 w-full p-6 bg-gradient-to-t from-zinc-950 via-zinc-950/80 to-transparent z-20">
                <div className="max-w-3xl mx-auto relative group">
                    <div className="absolute -inset-0.5 bg-gradient-to-r from-teal-500/20 to-indigo-500/20 rounded-full blur opacity-50 group-hover:opacity-100 transition duration-700"></div>
                    <form
                        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
                        className="relative flex items-center bg-zinc-900/90 backdrop-blur-xl rounded-full border border-zinc-800 shadow-2xl overflow-hidden focus-within:border-zinc-700 transition-all p-2"
                    >
                        <input
                            ref={inputRef}
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask a question..."
                            className="w-full bg-transparent pl-6 pr-4 py-3 text-zinc-100 placeholder-zinc-600 focus:outline-none text-base font-light"
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            disabled={!input.trim() || isLoading}
                            className="p-3 rounded-full bg-zinc-100 text-zinc-900 hover:bg-zinc-300 disabled:opacity-50 disabled:hover:bg-zinc-100 transition-all shadow-lg"
                        >
                            {isLoading ? <span className="block w-4 h-4 border-2 border-zinc-900 border-t-transparent rounded-full animate-spin" /> : <ArrowUp size={20} />}
                        </button>
                    </form>
                </div>
                <p className="text-center text-zinc-700 text-[10px] mt-4 tracking-wider uppercase">
                    Generated content may be inaccurate.
                </p>
            </div>
        </main>
    );
};

export default ChatWindow;
