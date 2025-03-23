import React from "react";

type PaginationProps = {
  page: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
  hasSearchQuery: boolean;
};

const Pagination: React.FC<PaginationProps> = ({
  page,
  setPage,
  hasSearchQuery,
}) => {
  if (hasSearchQuery) return null;

  return (
    <div className="flex justify-between mt-8">
      <button
        className="px-4 py-2 border border-black text-black hover:bg-black hover:text-white disabled:opacity-50 cursor-pointer"
        onClick={() => setPage((prev) => Math.max(prev - 1, 0))}
        disabled={page === 0}
      >
        Previous
      </button>
      <button
        className="px-4 py-2 border border-black text-black hover:bg-black hover:text-white cursor-pointer"
        onClick={() => setPage((prev) => prev + 1)}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;
