import {Routes,Route} from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Overview from './pages/Overview';
import SearchPage from './pages/Search';
import Library from './pages/Library';
import Analytics from './pages/Analytics';
import Admin from './pages/Admin';
export default function App(){return <div className="app-shell"><Sidebar/><main className="main-content"><Routes><Route path="/" element={<Overview/>}/><Route path="/search" element={<SearchPage/>}/><Route path="/library" element={<Library/>}/><Route path="/analytics" element={<Analytics/>}/><Route path="/admin" element={<Admin/>}/><Route path="*" element={<Overview/>}/></Routes><footer className="footer"><span>RESEARCHLENS © 2026</span><span>Academic discovery, powered by information retrieval.</span></footer></main></div>}
