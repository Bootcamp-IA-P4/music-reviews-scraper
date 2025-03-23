"use client";

import { useEffect, useState } from "react";

type Review = {
  id: number;
  artist: string;
  title: string;
  genre: string;
  rating: number;
  label: string;
  reviewer: string;
};

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [searchArtist, setSearchArtist] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const fetchReviews = () => {
    setLoading(true);
    const params = searchQuery
      ? `artist=${encodeURIComponent(searchQuery)}`
      : `limit=50&offset=${page * 50}`;

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/reviews?${params}`)
      .then((res) => res.json())
      .then((data) => setReviews(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReviews();
  }, [page, searchQuery]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(0); // reset page when searching
    setSearchQuery(searchArtist);
  };

  return (
    <main className="max-w-5xl mx-auto p-8 bg-white text-black font-serif">
      <h1 className="text-4xl font-light mb-8 border-b pb-4">
        Pitchfork Reviews
      </h1>

      {/* 🔎 Search */}
      <form onSubmit={handleSearch} className="mb-8 flex gap-4">
        <input
          type="text"
          placeholder="Search by artist..."
          value={searchArtist}
          onChange={(e) => setSearchArtist(e.target.value)}
          className="border border-black px-4 py-2 w-full"
        />
        <button
          type="submit"
          className="border border-black px-6 py-2 hover:bg-black hover:text-white"
        >
          Search
        </button>
      </form>

      {/* 📄 Reviews */}
      {loading ? (
        <p>Loading reviews...</p>
      ) : reviews.length === 0 ? (
        <p>No reviews found.</p>
      ) : (
        <ul className="space-y-6">
          {reviews.map((review) => (
            <li key={review.id} className="border-b pb-4">
              <h2 className="text-2xl font-light">
                {review.title} — <span className="italic">{review.artist}</span>
              </h2>
              <p className="text-sm text-gray-600">
                Genre: {review.genre} | Label: {review.label} | Score:{" "}
                {review.rating}/10
              </p>
              <p className="text-xs text-gray-500">By {review.reviewer}</p>
            </li>
          ))}
        </ul>
      )}

      {/* Pagination */}
      {!searchQuery && (
        <div className="flex justify-between mt-8">
          <button
            className="px-4 py-2 border border-black text-black hover:bg-black hover:text-white disabled:opacity-50"
            onClick={() => setPage((prev) => Math.max(prev - 1, 0))}
            disabled={page === 0}
          >
            Previous
          </button>
          <button
            className="px-4 py-2 border border-black text-black hover:bg-black hover:text-white"
            onClick={() => setPage((prev) => prev + 1)}
          >
            Next
          </button>
        </div>
      )}
    </main>
  );
}
