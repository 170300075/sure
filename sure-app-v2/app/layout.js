import "@styles/globals.css"

import {Inter} from "next/font/google"

const inter = Inter({
  subsets: ["latin"]
})

export const metadata = {
  title: 'Syno International',
  charset: 'UTF-8',
  description: 'Providing connected people data with speed and efficiency',
  icons: {
    icon: "./favicon.ico"
  }
}
 
export default function RootLayout({ children }) {
 return (
    <html lang="en" className={`${inter.className} h-full bg-white`}>
      <body className="h-full">{children}</body>
    </html>
  )
}