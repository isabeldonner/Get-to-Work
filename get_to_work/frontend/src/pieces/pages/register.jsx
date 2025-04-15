import React from 'react'
import {useNavigate} from 'react-router-dom'
import './login.jsx'
import './login.css'

import user_icon from '../assets/user.png'
import password_icon from '../assets/locked-computer.png'
import email_icon from '../assets/email.png'
import leetcode_icon from '../assets/leetcode.png'

const Register = () => {
        const [username, setUsername] = React.useState("");
        const [email, setEmail] = React.useState("");
        const [password, setPassword] = React.useState("");
        const [leetcodeUser, setLeetcodeUser] = React.useState("");
        const navigate = useNavigate();
    
        const handleSubmit = async(event) => {
            event.preventDefault();
            const url = "http://localhost:8000/register/";
            
            const body = {username: username, email, password, leetcodeUser};
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
            navigate("/login");
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
            <div className = 'loginsign'>Register</div>
          </div>
          <div className = 'inputs'>
            <div className = 'input'>
                <img src = {user_icon} className = 'icon' alt = ''/>
                <input type = 'text' placeholder = 'Username' value = {username} onChange = {(e)=>setUsername(e.target.value)}/> 
            </div>
            <div className = 'input'>
                <img src = {email_icon} className = 'icon' alt = ''/>
                <input type = 'text' placeholder = 'Email' value = {email} onChange = {(e)=>setEmail(e.target.value)}/>
            </div>
            <div className = 'input'>
                <img src = {password_icon} className = 'icon' alt = ''/>
                <input type = 'text' placeholder = 'Password' value = {password} onChange = {(e)=>setPassword(e.target.value)}/> 
            </div>
            <div className = 'input'>
                <img src = {leetcode_icon} className = 'icon' alt = ''/>
                <input type = 'text' placeholder = 'Leetcode Username' value = {leetcodeUser} onChange = {(e)=>setLeetcodeUser(e.target.value)}/> 
            </div>
          </div>
            <div className = 'submit-container'>
              <form onSubmit = {handleSubmit}>
                <button className = 'submit' type = 'submit'>Register</button>
              </form>
                <div className = 'acct'>Already have an account? <span className = 'existing' onClick = {() => navigate('/login')}>Log in</span></div>
                
            </div>
        </div>
      ) 

}

export default Register