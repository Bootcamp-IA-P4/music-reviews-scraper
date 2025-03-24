import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Pitchfork Review Recommender",
  description: "By Andrea Alonso Corbeira",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* 🔥 Header fijo */}
        <header className="fixed top-0 left-0 w-full border-b border-gray-200 bg-white z-50 text-center text-sm text-gray-600 py-4">
          <Link href="/" className="text-gray-700 font-serif hover:text-black">
            Pitchfork Review Recommender
          </Link>
        </header>
        {/* 🚀 Main centrado, compensando el header fijo */}
        <main className="max-w-5xl mx-auto px-8 mt-14 bg-white text-black font-serif">
          {children}
        </main>
        {/* 📌 Footer opcional */}
        <footer className="w-full border-t border-gray-200 p-4 text-center text-xs text-gray-500">
          © {new Date().getFullYear()} Proyecto sin ánimo de lucro
        </footer>{" "}
      </body>
    </html>
  );
}
