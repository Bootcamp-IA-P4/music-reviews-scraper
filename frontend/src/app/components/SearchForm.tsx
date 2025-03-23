import React from "react";

type SearchFormProps = {
  searchArtist: string;
  setSearchArtist: (value: string) => void;
  handleSearch: (e: React.FormEvent) => void;
};

const SearchForm: React.FC<SearchFormProps> = ({
  searchArtist,
  setSearchArtist,
  handleSearch,
}) => {
  return (
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
  );
};

export default SearchForm;
