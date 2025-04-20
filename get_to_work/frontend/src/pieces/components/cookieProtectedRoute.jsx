import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import '../pages/update.jsx';


const CookieProtectedRoute = () => {
    const isUpdated = localStorage.getItem("cookieUpdated");
    return isUpdated ? <Outlet /> : <Navigate to = "/update" replace/>;
};

export default CookieProtectedRoute;