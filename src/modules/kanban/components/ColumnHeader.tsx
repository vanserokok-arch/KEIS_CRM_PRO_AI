import React from 'react';

interface ColumnHeaderProps {
    title: string;
}

const ColumnHeader: React.FC<ColumnHeaderProps> = ({ title }) => {
    return (
        <div className="kan-col__header">
            <h4>{title}</h4>
        </div>
    );
};

export default ColumnHeader;
