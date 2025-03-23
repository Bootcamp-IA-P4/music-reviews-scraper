"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="h-screen flex flex-col items-center justify-center text-center -mt-28">
      <h1 className="text-4xl font-light mb-8 mb-8 border-b pb-4 max-w-2xl font-serif ">
        Welcome to your personal Pitchfork
      </h1>

      <p className="text-lg mb-8 text-gray-500 max-w-xl font-serif ">
        We mix your music taste with Pitchfork reviews so you can discover
        hidden gems. We won’t promise objectivity... but we’ll try to keep it
        fun.
      </p>

      <Link
        href="/reviews"
        className="border border-black text-white bg-black px-6 py-3 hover:bg-white hover:text-black transition-colors font-serif w-full md:w-auto cursor-pointer my-2 inline-block"
      >
        Start discovering
      </Link>

      <p className="text-xs text-gray-500 mt-12">
        Made with love and a bit of code.
      </p>
    </div>
  );
}
