import { NextResponse } from 'next/server';

global.requestLogs = global.requestLogs || [];

export async function GET() {
  global.requestLogs.push({
    method: 'GET',
    path: '/api/test',
    timestamp: new Date().toISOString()
  });
  return NextResponse.json({ status: 'ok' });
}

export async function POST(request) {
  const body = await request.json();
  const log = {
    method: 'POST',
    path: '/api/test',
    body,
    timestamp: new Date().toISOString()
  };
  global.requestLogs.push(log);
  console.log('POST /api/test', body);
  
  return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
}
