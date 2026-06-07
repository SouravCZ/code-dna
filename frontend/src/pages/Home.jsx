import React from 'react';
import SearchBar from '../components/SearchBar';

function Home({ onSearch, loading }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <div className="text-center mb-8">
        <h1 className="text-6xl font-bold gradient-text mb-4">Code DNA 🧬</h1>
        <p className="text-2xl text-gray-300 mb-2">Discover Your Developer Identity</p>
        <p className="text-gray-400">Enter any GitHub username to generate a personalized developer DNA card</p>
      </div>
      
      <div className="w-full max-w-2xl px-4">
        <SearchBar onSearch={onSearch} loading={loading} />
      </div>

      <div className="mt-16 grid md:grid-cols-3 gap-8 max-w-4xl">
        <div className="text-center">
          <div className="text-4xl mb-3">🔍</div>
          <h3 className="text-xl font-semibold text-white mb-2">Analyze</h3>
          <p className="text-gray-400">We analyze your GitHub profile including repos, languages, and commit history</p>
        </div>
        <div className="text-center">
          <div className="text-4xl mb-3">🤖</div>
          <h3 className="text-xl font-semibold text-white mb-2">AI-Powered</h3>
          <p className="text-gray-400">Advanced AI generates insights about your coding style and personality</p>
        </div>
        <div className="text-center">
          <div className="text-4xl mb-3">✨</div>
          <h3 className="text-xl font-semibold text-white mb-2">Beautiful Card</h3>
          <p className="text-gray-400">Get a stunning, shareable developer DNA card with your unique profile</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
