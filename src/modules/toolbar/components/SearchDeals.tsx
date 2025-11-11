import React, { useState } from 'react';

const SearchDeals: React.FC = () => {
    const [query, setQuery] = useState('');

    return (
        <input 
            type="text" 
            placeholder="Поиск по сделкам..." 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
        />
    );
};

export default SearchDeals;
