import './globals.css';

export const metadata = {
  title: 'Microservices Load Test',
  description: 'Load testing tool',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
