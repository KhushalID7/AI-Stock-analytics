import React, { useState } from 'react';
import axios from 'axios';

const ChatInterface: React.FC = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState<string | null>(null);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        try {
            const res = await axios.post('/api/chat', { query });
            setResponse(res.data);
        } catch (error) {
            console.error('Error fetching data:', error);
            setResponse('Error fetching data');
        }
    };

    return (
        <div className="chat-interface">
            <form onSubmit={handleSubmit} className="flex flex-col">
                <input
                    type="text"
                    value={query}
                    onChange={handleInputChange}
                    placeholder="Ask about stock data..."
                    className="border p-2 mb-2"
                />
                <button type="submit" className="bg-blue-500 text-white p-2">
                    Submit
                </button>
            </form>
            {response && <div className="response mt-4">{response}</div>}
        </div>
    );
};

export default ChatInterface;