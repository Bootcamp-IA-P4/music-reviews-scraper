"use client";

export default function SpotifyLoginButton() {
  const handleLogin = () => {
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/login`;
  };

  return (
    <div className="flex flex-col items-center mb-12 flex gap-2">
      <p className="text-xs text-gray-500">Or maybe...</p>
      <button
        onClick={handleLogin}
        className="border border-black text-white bg-black px-6 py-3 hover:bg-white hover:text-black transition-colors font-serif w-full md:w-auto cursor-pointer my-2"
      >
        Would you prefer a personalized recommendation?
      </button>
      <p className="text-xs text-gray-500">
        Connect with your Spotify account and find out if your saved albums (or
        other albums by these artists) already have a music review in your
        favorite music magazine.
      </p>
    </div>
  );
}
