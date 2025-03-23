"use client";

import { useEffect, useState } from "react";
import SpotifyLoginButton from "../components/SpotifyLoginButton";
import SearchForm from "../components/SearchForm";
import ReviewList, { Review } from "../components/ReviewList";
import Pagination from "../components/Pagination";

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
    <>
      <h1 className="text-4xl font-light mb-12 border-b pb-4 pt-12">
        Pitchfork Album Reviews
      </h1>

      {/* 🔎 Search */}
      <SearchForm
        searchArtist={searchArtist}
        setSearchArtist={setSearchArtist}
        handleSearch={handleSearch}
      />

      {/* 🎵 Spotify Login */}
      <SpotifyLoginButton />

      {/* 📄 Reviews */}
      <ReviewList reviews={reviews} loading={loading} />

      {/* Pagination */}
      <Pagination
        page={page}
        setPage={setPage}
        hasSearchQuery={!!searchQuery}
      />

      <div className="h-20" />
    </>
  );
}
