import React from 'react';

interface ColumnProps {
    title: string;
}

const Column: React.FC<ColumnProps> = ({ title }) => {
    return (
        <div className="kan-col">
            <h3>{title}</h3>
            {/* Placeholder for DealCards */}
        </div>
    );
};

export default Column;
