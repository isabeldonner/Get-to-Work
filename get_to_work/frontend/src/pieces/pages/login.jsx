import React from 'react'
import {useNavigate} from 'react-router-dom'
import './register.jsx'
import './update.jsx'
import './login.css'

import user_icon from '../assets/user.png'
import password_icon from '../assets/locked-computer.png'



const Login = () => {

    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");
    const navigate = useNavigate();

    const handleSubmit = async(event) => {
        event.preventDefault();
        const url = "http://localhost:8000/login/";
        
        const body = {username, password};
        try{
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
          });
        
          const data = await response.json();
      if (response.ok) { 
        alert(data.message);
        if(data.token){
          localStorage.setItem("authToken", data.token);
          localStorage.setItem("username", username);
          navigate("/update");
        }
      } else {
        alert(data.detail);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong. Try again.");
    }

      };
  return (
    <div className = 'container'>
      <div className = 'header'>
        <div className = 'text'>Get to Work!</div>
        <div className = 'loginsign'>Log In</div>
      </div>
      <div className = 'inputs'>
        <div className = 'input'>
            <img src = {user_icon} className = 'icon' alt = ''/>
            <input type = 'text' placeholder = 'Username or email' value = {username} onChange = {(e)=>setUsername(e.target.value)}/> 
        </div>
        <div className = 'input'>
            <img src = {password_icon} className = 'icon' alt = ''/>
            <input type = 'password' placeholder = 'Password' value = {password} onChange = {(e)=>setPassword(e.target.value)}/> 
        </div>
      </div>
        <div className = 'submit-container'>
          <form onSubmit = {handleSubmit}>
            <button className = 'submit' type = 'submit'>Log In</button>
          </form>
            <div className = 'acct'>New to Get to Work? <span className = 'existing' onClick ={()=>navigate("/register")}>Create an account</span></div>
        </div>
    </div>
  ) 
}

export default Login