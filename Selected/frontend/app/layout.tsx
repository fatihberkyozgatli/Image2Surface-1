import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Image2Surface - 3D Surface Generator',
  description: 'Convert images to 3D surfaces with interactive editing',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  )
}
