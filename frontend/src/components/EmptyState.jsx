import {SearchX} from 'lucide-react';
export default function EmptyState({title='No papers found',message='Import a dataset or try another search query.'}){return <div className="empty-state"><SearchX size={28}/><b>{title}</b><p>{message}</p></div>}
