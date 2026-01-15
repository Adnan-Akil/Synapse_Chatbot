import { Upload, FileText, X, CheckCircle2 } from 'lucide-react';
import { AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import axios from 'axios';

const Sidebar = ({ isOpen, toggleSidebar }) => {
  const [files, setFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (event) => {
    const uploadedFiles = Array.from(event.target.files);
    setIsUploading(true);

    for (const file of uploadedFiles) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            await axios.post('http://localhost:8000/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
             setFiles(prev => [...prev, file.name]);
        } catch (error) {
            console.error("Upload failed", error);
        }
    }
    setIsUploading(false);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleSidebar}
            className="absolute inset-0 bg-black/60 backdrop-blur-sm z-40"
          />

          {/* Drawer Panel (Right Side) */}
          <motion.aside
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="absolute right-0 top-0 h-full w-full max-w-sm bg-zinc-950 border-l border-zinc-800 shadow-2xl z-50 flex flex-col"
          >
            {/* Header */}
            <div className="p-8 flex items-center justify-between border-b border-zinc-900">
              <div>
                  <h2 className="text-xl font-light text-zinc-100">Documents</h2>
                  <p className="text-xs text-zinc-500 mt-1">Manage your context sources</p>
              </div>
              <button 
                onClick={toggleSidebar} 
                className="p-2 rounded-full hover:bg-zinc-900 text-zinc-500 hover:text-zinc-300 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            {/* Content */}
            <div className="p-8 flex-1 overflow-y-auto space-y-6 no-scrollbar">
              
              {/* Upload Dropzone */}
              <div className="space-y-3">
                  <span className="text-xs font-semibold text-zinc-600 uppercase tracking-widest pl-1">Add New</span>
                  <label className="relative flex flex-col items-center justify-center w-full h-32 border border-dashed border-zinc-800 rounded-xl hover:bg-zinc-900/50 hover:border-zinc-700 transition-all cursor-pointer group">
                    <div className="flex flex-col items-center gap-2">
                         <div className="p-3 bg-zinc-900 rounded-full group-hover:scale-110 transition-transform">
                             <Upload size={18} className="text-zinc-400 group-hover:text-teal-400 transition-colors" />
                         </div>
                         <span className="text-xs text-zinc-500 font-medium">
                            {isUploading ? 'Processing...' : 'Click to Upload'}
                         </span>
                    </div>
                    <input type="file" multiple className="hidden" onChange={handleFileUpload} disabled={isUploading} />
                  </label>
              </div>

              {/* File List */}
              <div className="space-y-3">
                 <span className="text-xs font-semibold text-zinc-600 uppercase tracking-widest pl-1">Library</span>
                 
                 {files.length === 0 ? (
                    <div className="py-8 text-center border border-zinc-900 rounded-xl bg-zinc-900/20">
                         <p className="text-sm text-zinc-600">No documents active</p>
                    </div>
                 ) : (
                    <div className="space-y-2">
                        {files.map((file, idx) => (
                            <motion.div 
                                initial={{ opacity: 0, y: 5 }}
                                animate={{ opacity: 1, y: 0 }}
                                key={idx} 
                                className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/30 hover:border-zinc-700 transition-colors"
                            >
                                <FileText size={16} className="text-teal-500/70" />
                                <span className="text-sm text-zinc-300 truncate flex-1">{file}</span>
                                <CheckCircle2 size={14} className="text-emerald-500/50" />
                            </motion.div>
                        ))}
                    </div>
                 )}
              </div>
            </div>

          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
};

export default Sidebar;
