import axios from 'axios';
const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api/v1',timeout:120000});
export const searchPapers=async payload=>(await api.post('/search',payload)).data;
export const getOverview=async()=>(await api.get('/analytics/overview')).data;
export const getTopics=async()=>(await api.get('/analytics/topics')).data;
export const getClusters=async()=>(await api.get('/analytics/clusters')).data;
export const getPapers=async params=>(await api.get('/papers',{params})).data;
export const importPapers=async limit=>(await api.post('/admin/import',null,{params:{limit}})).data;
export const getHealth=async()=>(await api.get('/health')).data;
