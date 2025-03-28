import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import '../pages/login.jsx';


const ProtectedRoute = () => {
    const isAuthenticated = localStorage.getItem("authToken");
    console.log("Auth Token:", isAuthenticated);
    return isAuthenticated ? <Outlet /> : <Navigate to = "/login" replace/>;
};

export default ProtectedRoute;