import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Board from '../modules/kanban/components/Board';
import DealsTable from '../modules/list/components/DealsTable';

const AppRoutes: React.FC = () => {
    return (
        <Routes>
            <Route path="/kanban" element={<Board />} />
            <Route path="/list" element={<DealsTable />} />
            {/* Additional routes can be defined here */}
        </Routes>
    );
};

export default AppRoutes;
