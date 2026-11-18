import { NavLink } from 'react-router-dom';
import {
  BookOpen,
  Search,
  ChartNoAxesCombined,
  Database,
  Code2
} from 'lucide-react';
const links=[['/','Overview',ChartNoAxesCombined],['/search','Discover papers',Search],['/library','Paper library',BookOpen],['/analytics','Text analytics',ChartNoAxesCombined],['/admin','Dataset manager',Database]];
export default function Sidebar(){return <aside className="sidebar"><div className="brand"><div className="brand-mark">R</div><div><b>ScholarlyX</b><small>ACADEMIC INTELLIGENCE</small></div></div><div className="side-label">WORKSPACE</div><nav>{links.map(([to,label,Icon])=><NavLink key={to} to={to} end={to==='/'} className={({isActive})=>`nav-link ${isActive?'active':''}`}><Icon size={18}/><span>{label}</span></NavLink>)}</nav><div className="sidebar-bottom"><div className="mini-status"><i/>Research engine ready<small>Local workspace</small></div><a className="nav-link" href="https://github.com/aaryancodebase/ResearchLens" target="_blank" rel="noreferrer"><Code2 size={17}/>GitHub repository</a></div></aside>}
