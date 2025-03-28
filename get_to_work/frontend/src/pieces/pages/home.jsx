import React, {useEffect, useState} from 'react'
import {useNavigate} from 'react-router-dom'
import './login.jsx'

const Home = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    useEffect(() => {
    const token = localStorage.getItem("authToken");

    if (!token) {
      alert("You must be logged in to access this page.");
      navigate("/login");
    } else{
        setLoading(false);
    }
  }, [navigate]);
    if(loading){
        return null;
    }
    return (
        <div>
            <h1>Home</h1>
        </div>
    )
}

export default Home