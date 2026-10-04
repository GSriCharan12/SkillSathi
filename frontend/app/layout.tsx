import type { Metadata } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { ErrorBoundary } from "@/components/feedback/ErrorBoundary";

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "SkillSathi | Explore a future your whole family believes in",
  description:
    "AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education in India.",
  keywords: [
    "Vocational Education India",
    "SkillSathi",
    "Family Career Counselling",
    "ITI Lateral Entry",
    "B.Voc Pathways",
    "NSQF",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={plusJakartaSans.variable}>
      <body className="min-h-screen flex flex-col antialiased selection:bg-[#2A9D8F]/20 selection:text-[#14213D] garden-gradient-hero">
        <ErrorBoundary>
          <Navbar />
          <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {children}
          </main>
          <Footer />
        </ErrorBoundary>
      </body>
    </html>
  );
}
