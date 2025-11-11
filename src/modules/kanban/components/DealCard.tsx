import React from 'react';

interface DealCardProps {
    title: string;
}

const DealCard: React.FC<DealCardProps> = ({ title }) => {
    return (
        <div className="kan-card">
            <h5>{title}</h5>
            {/* Placeholder for additional deal information */}
        </div>
    );
};

export default DealCard;
