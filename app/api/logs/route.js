import { NextResponse } from 'next/server';

global.requestLogs = global.requestLogs || [];

export async function GET() {
  return NextResponse.json(global.requestLogs);
}
