"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import SearchForm from "../components/SearchForm";
import ReviewList, { Review } from "../components/ReviewList";

export default function RecommendedPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchArtist, setSearchArtist] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const searchParams = useSearchParams();
  const spotifyUserId = searchParams.get("spotify_user_id");

  const fetchReviews = () => {
    if (!spotifyUserId) return;

    setLoading(true);

    const params = new URLSearchParams();
    params.append("spotify_user_id", spotifyUserId || "");

    if (searchQuery) {
      params.append("artist", searchQuery);
    }

    fetch(
      `${
        process.env.NEXT_PUBLIC_API_URL
      }/recommended_reviews?${params.toString()}`
    )
      .then((res) => res.json())
      .then((data) => setReviews(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (spotifyUserId) fetchReviews();
  }, [searchQuery, spotifyUserId]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchQuery(searchArtist);
  };

  return (
    <>
      <h1 className="text-4xl font-light mb-12 border-b pb-4 pt-12">
        Pitchfork Reviews For You
      </h1>

      {/* 🔎 Search */}
      <SearchForm
        searchArtist={searchArtist}
        setSearchArtist={setSearchArtist}
        handleSearch={handleSearch}
      />

      {!loading && reviews.length > 0 && (
        <p className="text-lg mb-6 text-gray-500">
          Whoa! Looks like there are {reviews.length} reviews you might find
          interesting 🎧
        </p>
      )}

      {/* 📄 Reviews */}
      <ReviewList reviews={reviews} loading={loading} />

      <div className="h-20" />
    </>
  );
}
