'use client';
import { useEffect, useState } from 'react';
export default function RevenuePage() {
  const [data, setData] = useState([]);
  useEffect(() => { fetch('/api/revenue/history').then(r=>r.json()).then(setData); }, []);
  return <div><h2>Revenue History</h2><pre>{JSON.stringify(data,null,2)}</pre></div>;
}
