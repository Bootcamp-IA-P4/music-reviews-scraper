import React from "react";

export type Review = {
  id: number;
  artist: string;
  title: string;
  genre: string;
  rating: number;
  label: string;
  reviewer: string;
  url: string;
};

type ReviewListProps = {
  reviews: Review[];
  loading: boolean;
};

const ReviewList: React.FC<ReviewListProps> = ({ reviews, loading }) => {
  if (loading) {
    return <p>Cargando...</p>;
  }

  if (reviews.length === 0) {
    return <p>No se encontraron coicidencias.</p>;
  }

  return (
    <ul className="space-y-6">
      {reviews.map((review) => (
        <li key={review.id} className="border-b pb-4">
          <a
            href={review.url}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline cursor-pointer"
          >
            <h2 className="text-2xl font-light">
              {review.title} — <span className="italic">{review.artist}</span>
            </h2>
          </a>
          <p className="text-sm text-gray-600">
            Genre: {review.genre} | Label: {review.label} | Score:{" "}
            {review.rating}/10
          </p>
          <p className="text-xs text-gray-500">By {review.reviewer}</p>
        </li>
      ))}
    </ul>
  );
};

export default ReviewList;
