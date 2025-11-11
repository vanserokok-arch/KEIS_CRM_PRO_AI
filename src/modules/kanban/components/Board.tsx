import React from 'react';
import Column from './Column';

const Board: React.FC = () => {
    return (
        <div className="kanban-board">
            <Column title="Новые" />
            <Column title="В работе" />
            <Column title="Досудебные" />
            <Column title="Судебные" />
            <Column title="Завершенные" />
        </div>
    );
};

export default Board;
